import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "development")))

import logging
import queue
import time
from datetime import datetime

import cv2 as cv
import numpy as np
from ultralytics import checks as ultralytics_checks

from app.core.db import get_db
from app.repositories.r_item import RItem
from app.repositories.r_user import RUser
from app.schemas import ItemCreate
from app.services.s_item import SItem
from app.services.s_user import SUser

from .counter import Counter as ObjectCounter
from .state import State
from .utils import crop_and_mask_image, stack_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Predictor:
    def __init__(
        self,
        state: State,
        buffer: State,
        counter: ObjectCounter,
        border_xy: tuple[int, int, int, int],
        line_in: np.ndarray,
        line_out: np.ndarray,
        polygon: np.ndarray,
        is_counter=True,
        is_stream=True,
        verbose=0,
    ):
        self.state = state
        self.buffer = buffer
        self.counter = counter
        self.border_xy = border_xy
        self.x_min, self.y_min, self.x_max, self.y_max = border_xy
        self.line_in = line_in
        self.line_out = line_out
        self.polygon = polygon
        self.is_counter = is_counter
        self.is_stream = is_stream
        self.verbose = verbose

        if self.verbose:
            logger.info(ultralytics_checks())

    def display_counts(self, plot_im: np.ndarray, show_in=True, show_out=True):
        """Override ObjectCounter display_counts"""
        labels_dict = {
            str.capitalize(key): f"{'IN ' + str(value['IN']) if show_in else ''} "
            f"{'OUT ' + str(value['OUT']) if show_out else ''}".strip()
            for key, value in self.counter.classwise_counts.items()
            if value["IN"] != 0 or value["OUT"] != 0
        }
        if labels_dict:
            self.counter.annotator.display_analytics(
                plot_im,
                labels_dict,
                (104, 31, 17),
                (255, 255, 255),
                self.counter.margin,
            )

    def run(self):
        # fps
        prev_time = time.time()
        while self.state.running.is_set():
            try:
                frame = self.state.queue.get(timeout=1)
            except queue.Empty:
                continue
            if frame is None:
                continue
            im1 = frame.copy()

            if self.is_counter:
                # counter
                im1 = crop_and_mask_image(
                    im1, self.x_min, self.y_min, self.x_max, self.y_max, self.polygon
                )

                # track and predict
                with self.counter.lock:
                    with self.counter.profilers[1]:
                        result, list_counted = self.counter.process(im1)

                    # show solution speed
                    track_or_predict = (
                        "predict"
                        if type(self.counter).__name__ == "ObjectCropper"
                        else "track"
                    )
                    track_or_predict_speed = self.counter.profilers[0].dt * 1e3
                    solution_speed = (
                        self.counter.profilers[1].dt - self.counter.profilers[0].dt
                    ) * 1e3  # solution time = process - track
                    result.speed = {
                        track_or_predict: track_or_predict_speed,
                        "solution": solution_speed,
                    }
                    if self.verbose:
                        self.counter.frame_no += 1
                        logger.info(
                            f"{self.counter.frame_no}: {result.plot_im.shape[0]}x{result.plot_im.shape[1]} {solution_speed:.1f}ms\n"
                            f"Speed: {track_or_predict_speed:.1f}ms {track_or_predict}, "
                            f"{solution_speed:.1f}ms solution per image at shape "
                            f"(1, {getattr(self.counter.model, 'ch', 3)}, {result.plot_im.shape[0]}, {result.plot_im.shape[1]})\n"
                        )
                # save item into database
                if list_counted:
                    logger.info(list_counted)
                    for counted in list_counted:
                        self.commit_item(*counted)

                # re-construct cropped frame into original frame
                im1 = stack_image(
                    frame,
                    result.plot_im,
                    self.x_min,
                    self.y_min,
                    self.x_max,
                    self.y_max,
                )

                # add fps
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time)
                prev_time = curr_time
                cv.putText(
                    im1,
                    f"FPS: {fps:.0f}",
                    (50, 50),
                    cv.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3,
                )

                # add counts
                self.display_counts(im1)

                # save frame as bytes for streaming
                if self.is_stream:
                    try:
                        _, buffer = cv.imencode(".jpg", frame)
                        frame_bytes = buffer.tobytes()
                        self.buffer.queue.put(frame_bytes, timeout=1)
                    except queue.Full:
                        logger.warning("⚠️ Queue full, dropping frame..")

    def commit_item(
        self,
        id_track: int,
        date_stamped: datetime,
        id_cls: int,
        conf: float,
        is_out: bool,
        is_up=False,
    ):
        with get_db() as session:
            repository = RUser(session)
            service = SUser(repository)
            user = service.read_users(skip=0, limit=1)

            repository = RItem(session)
            service = SItem(repository)

            item = ItemCreate(
                date_stamped=date_stamped,
                id_track=id_track,
                id_cls=id_cls,
                is_out=is_out,
                is_up=is_up,
            )
            return service.create_item(item, user.data[0].id)

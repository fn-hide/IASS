import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "development")))
from utils import crop_and_mask_image, stack_image

import queue
import time
import logging
import cv2 as cv
import numpy as np
from ultralytics import checks as ultralytics_checks
# from ultralytics.solutions import ObjectCounter

from vehicle_state import state
from vehicle_base import VehicleBase as ObjectCounter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VehicleCounter:
    def __init__(
        self,
        counter: ObjectCounter,
        border_xy: tuple[int, int, int, int],
        line_in: np.ndarray,
        line_out: np.ndarray,
        polygon: np.ndarray,
        is_counter=True,
        verbose=0,
    ):
        self.counter = counter
        self.border_xy = border_xy
        self.x_min, self.y_min, self.x_max, self.y_max = border_xy
        self.line_in = line_in
        self.line_out = line_out
        self.polygon = polygon
        self.is_counter = is_counter
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
        # show
        if self.verbose:
            cv.namedWindow("Ultralytics Solutions", cv.WINDOW_NORMAL)

        # fps
        prev_time = time.time()
        while state.running.is_set():
            try:
                frame = state.queue.get(timeout=1)
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
                result, list_counted = self.counter.process(im1)
                logger.info(list_counted)
                im1 = stack_image(
                    frame,
                    result.plot_im,
                    self.x_min,
                    self.y_min,
                    self.x_max,
                    self.y_max,
                )

            # fps
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time

            # show
            if self.verbose:
                self.display_counts(im1)
                cv.putText(
                    im1,
                    f"FPS: {fps:.0f}",
                    (50, 50),
                    cv.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3,
                )
                cv.imshow("Ultralytics Solutions", im1)
                if cv.waitKey(1) & 0xFF == ord("q"):
                    state.running.clear()
                    break
        if self.verbose:
            cv.destroyAllWindows()

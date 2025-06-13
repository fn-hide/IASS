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
from ultralytics.solutions import ObjectCounter

from vehicle_state import state


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
        verbose=0,
    ):
        self.counter = counter
        self.border_xy = border_xy
        self.x_min, self.y_min, self.x_max, self.y_max = border_xy
        self.line_in = line_in
        self.line_out = line_out
        self.polygon = polygon
        self.verbose = verbose

        if self.verbose:
            logger.info(ultralytics_checks())

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

            # counter
            im1 = crop_and_mask_image(
                im1, self.x_min, self.y_min, self.x_max, self.y_max, self.polygon
            )
            result = self.counter.process(im1)
            im1 = stack_image(
                frame, result.plot_im, self.x_min, self.y_min, self.x_max, self.y_max
            )

            # fps
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time

            # show
            if self.verbose:
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

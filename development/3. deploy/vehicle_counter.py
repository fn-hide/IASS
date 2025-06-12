import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "development")))

import time
import logging
import ultralytics
import cv2 as cv
import numpy as np
from ultralytics.solutions import ObjectCounter

from utils import crop_and_mask_image, stack_image, adjust_site_region

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VehicleCounter:
    def __init__(
        self,
        url: str,
        counter: ObjectCounter,
        border_xy: tuple[int, int, int, int],
        line_in: np.ndarray,
        line_out: np.ndarray,
        polygon: np.ndarray,
        buffer=3,
        fps=20,
        verbose=0,
    ):
        self.url = url
        self.counter = counter
        self.border_xy = border_xy
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.line_in = line_in
        self.line_out = line_out
        self.polygon = polygon
        self.buffer = buffer
        self.fps = fps
        self.verbose = verbose

        if self.verbose:
            logger.info(ultralytics.checks())
            logger.info(cv.getBuildInformation())

    def run(self):
        cap = cv.VideoCapture(self.url, cv.CAP_FFMPEG)
        cap.set(
            cv.CAP_PROP_BUFFERSIZE, self.buffer
        )  # Kurangi buffer agar tidak terlalu tertinggal
        cap.set(cv.CAP_PROP_FPS, self.fps)  # Sesuaikan dengan FPS stream
        if not cap.isOpened():
            logger.error("Error: Couldn't open RTSP stream")
            exit()

        prev_time = time.time()
        cv.namedWindow("Ultralytics Solutions", cv.WINDOW_NORMAL)
        while cap.isOpened():
            cap.grab()
            success, im0 = cap.read()
            if not success:
                logger.info(
                    "Video frame is empty or video processing has been successfully completed."
                )
                break

            im1 = im0.copy()
            im1 = crop_and_mask_image(
                im1, self.x_min, self.y_min, self.x_max, self.y_max, polygon
            )

            result = self.counter.process(im1)
            im1 = stack_image(im0, result.plot_im, x_min, y_min, x_max, y_max)

            # Calculate fps
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            cv.putText(
                im1,
                f"FPS: {fps:.0f}",
                (50, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3,
            )

            # Show manually without ultralytics solution because we need to merge with original image
            # Press 'q' to exit
            cv.imshow("Ultralytics Solutions", im1)
            if cv.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    line_in = None
    line_out = [[839, 20], [1157, 1333]]
    polygon = [[1157, 72], [1516, 278], [854, 1101], [707, 146]]
    (x_min, y_min, x_max, y_max), polygon, line_in, line_out = adjust_site_region(
        polygon, line_in, line_out
    )

    counter = ObjectCounter(
        region=line_out,  # Pass region points
        model="../asset/result/data_yolo11m_100/detect/train/weights/best.pt",  # model="yolo11n-obb.pt" for object counting using YOLO11 OBB model.
        show=False,  # Display the output
        show_in=True,  # Display in counts
        show_out=True,  # Display out counts
        line_width=1,  # Adjust the line width for bounding boxes and text display
    )

    count_vehicle = VehicleCounter(
        "rtsp://huda:Burunghudhud112@192.168.50.250:554/Streaming/Channels/101/",
        counter,
        (x_min, y_min, x_max, y_max),
        line_in,
        line_out,
        polygon,
    )

    count_vehicle.run()

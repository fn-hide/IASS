import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "development")))

import logging
import cv2 as cv

from utils import adjust_site_region

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Stream:
    def __init__(
        self,
        url: str,
        buffer=3,
        fps=20,
    ):
        self.url = url
        self.buffer = buffer
        self.fps = fps

    def run(self) -> None:
        cap = cv.VideoCapture(self.url, cv.CAP_FFMPEG)
        cap.set(
            cv.CAP_PROP_BUFFERSIZE, self.buffer
        )  # Kurangi buffer agar tidak terlalu tertinggal
        cap.set(cv.CAP_PROP_FPS, self.fps)  # Sesuaikan dengan FPS stream
        if not cap.isOpened():
            logger.error("Error: Couldn't open RTSP stream")
            exit()

        cv.namedWindow("CCTV", cv.WINDOW_NORMAL)
        while cap.isOpened():
            cap.grab()
            success, im0 = cap.read()
            if not success:
                logger.info(
                    "Video frame is empty or video processing has been successfully completed."
                )
                break

            (
                (x_min, y_min, x_max, y_max),
                polygon,
                line_in,
                line_out,
            ) = adjust_site_region(self.polygon, self.line_in, self.line_out)
            cv.imshow("CCTV", im0)

            # Press 'q' to exit
            if cv.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    stream = Stream(
        "rtsp://huda:Burunghudhud112@192.168.50.250:554/Streaming/Channels/101/",
        buffer=1,
        fps=20,
    )
    stream.run()

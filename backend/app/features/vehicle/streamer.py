import logging
import queue

import cv2 as cv

from .state import State

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Streamer:
    def __init__(
        self,
        state_counting: State,
        url: str,
        fps: int,
        buffer: int,
    ):
        self.state_counting = state_counting
        self.url = url
        self.buffer = buffer
        self.fps = fps

        self.cap = None

    def run(self):
        logger.info("🚀 Stream started")
        self.cap = cv.VideoCapture(self.url, cv.CAP_FFMPEG)
        self.cap.set(cv.CAP_PROP_BUFFERSIZE, self.buffer)
        self.cap.set(cv.CAP_PROP_FPS, self.fps)
        if not self.cap.isOpened():
            logger.error("❌ Error: Couldn't open RTSP stream")
            self.state_counting.running.clear()
            return

        i_frame = 0
        while self.state_counting.running.is_set():
            i_frame += 1
            if i_frame % 2 == 0:
                # logger.info("▶️ Reading frame..")
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning(
                        "⚠️ Video frame is empty or video processing has been successfully completed."
                    )
                    self.state_counting.running.clear()
                    break

                try:
                    self.state_counting.queue.put(frame, timeout=1)
                except queue.Full:
                    logger.warning("⚠️ Queue full, dropping frame..")
                    try:
                        self.state_counting.queue.get_nowait()
                    except queue.Empty:
                        pass
            else:
                # logger.info("⏯️ Skipping frame..")
                self.cap.grab()

        self.cap.release()
        logger.info("🔚 Stream stopped")

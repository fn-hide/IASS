import logging
import queue

import cv2 as cv

from .state import State

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Streamer:
    def __init__(
        self,
        state_streaming: State,
        url: str,
        buffer=3,
        fps=20,
    ):
        self.state_streaming = state_streaming
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
            self.state_streaming.running.clear()
            return

        i_frame = 0
        while self.state_streaming.running.is_set():
            i_frame += 1
            if i_frame % 2 == 0:
                # logger.info("▶️ Reading frame..")
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning(
                        "⚠️ Video frame is empty or video processing has been successfully completed."
                    )
                    self.state_streaming.running.clear()
                    break

                try:
                    self.state_streaming.queue.put(frame, timeout=1)
                except queue.Full:
                    logger.warning("⚠️ Queue full, dropping frame..")
            else:
                # logger.info("⏯️ Skipping frame..")
                self.cap.grab()

        self.cap.release()
        logger.info("🔚 Stream stopped")

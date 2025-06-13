import queue
import logging
import cv2 as cv

from vehicle_state import state


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VehicleStreamer:
    def __init__(
        self,
        url: str,
        buffer=3,
        fps=20,
    ):
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
            state.running.clear()
            return

        while state.running.is_set():
            ret, frame = self.cap.read()
            if not ret:
                logger.warning(
                    "⚠️ Video frame is empty or video processing has been successfully completed."
                )
                state.running.clear()
                break

            try:
                state.queue.put(frame, timeout=1)
            except queue.Full:
                logger.warning("⚠️ Queue full, dropping frame..")

        self.cap.release()
        logger.info("🔚 Stream stopped")

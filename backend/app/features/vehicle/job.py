import threading
import uuid

from ultralytics import YOLO

from app.features.vehicle.utils import adjust_site_region

from .counter import Counter as ObjectCounter
from .predictor import Predictor
from .state import State
from .streamer import Streamer


class Job:
    def __init__(
        self,
        url_stream: str,
        path_model: str,
        region_config: tuple,
        fps=20,
        buffer=1,
        is_stream=0,
        verbose=0,
    ):
        self.url_stream = url_stream
        self.path_model = path_model
        self.region_config = region_config
        self.fps = fps
        self.buffer = buffer
        self.is_stream = is_stream
        self.verbose = verbose

        self.thread_streamer = None
        self.thread_counter = None
        self.state_counting = State()
        self.state_streaming = State(maxsize=3)

    def start(self):
        (x_min, y_min, x_max, y_max), polygon, line_in, line_out = adjust_site_region(
            *self.region_config
        )

        model = YOLO(self.path_model)
        counter = ObjectCounter(
            region=line_out,
            model=model,
            show=False,
            show_in=False,
            show_out=False,
            line_width=2,
        )

        streamer = Streamer(self.state_counting, self.url_stream, self.fps, self.buffer)
        predictor = Predictor(
            self.state_counting,
            self.state_streaming,
            counter,
            (x_min, y_min, x_max, y_max),
            line_in,
            line_out,
            polygon,
            self.region_config,
            is_stream=self.is_stream,
            verbose=self.verbose,
        )

        self.thread_streamer = threading.Thread(target=streamer.run, daemon=True)
        self.thread_counter = threading.Thread(target=predictor.run, daemon=True)

        self.thread_streamer.start()
        self.thread_counter.start()

        print(f"💨 Stream started for {self.url_stream}")

    def stop(self, id: uuid.UUID):
        self.state_counting.running.clear()
        self.state_streaming.running.clear()
        self.thread_streamer.join()
        self.thread_counter.join()
        del JOBS[id]

        print(f"🗑️ Stream deleted for {self.url_stream}")


# store running jobs globally
JOBS: dict[uuid.UUID, Job] = {}


if __name__ == "__main__":
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "development")))
    from utils import adjust_site_region

    line_in = None
    line_out = [[839, 20], [1157, 1333]]
    polygon = [[1157, 72], [1516, 278], [854, 1101], [707, 146]]
    (x_min, y_min, x_max, y_max), polygon, line_in, line_out = adjust_site_region(
        polygon, line_in, line_out
    )

    model = YOLO("./asset/result/data_yolo11m_100/detect/train/weights/best.pt")
    counter = ObjectCounter(
        region=line_out,
        model=model,
        show=False,
        show_in=False,
        show_out=False,
        line_width=2,
    )

    # ip-nvr
    url = "rtsp://huda:Burunghudhud112@192.168.50.250:554/Streaming/Channels/101/"
    # ip-cam
    url = "rtsp://huda:Burunghudhud112@192.168.50.26:554/Streaming/Channels/101/"
    streamer = Streamer(url, 1, 20)
    predictor = Predictor(
        counter,
        (x_min, y_min, x_max, y_max),
        line_in,
        line_out,
        polygon,
        # False,
        verbose=1,
    )

    t1 = threading.Thread(target=streamer.run)
    t2 = threading.Thread(target=predictor.run)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("✅ Program exited gracefully")

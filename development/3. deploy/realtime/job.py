import threading
from ultralytics import YOLO
# from ultralytics.solutions import ObjectCounter

from streamer import Streamer
from predictor import Predictor
from counter import Counter as ObjectCounter


class VehicleJob:
    def __init__(self, url_stream: str, path_model: str, region_config):
        self.url_stream = url_stream
        self.path_model = path_model
        self.region_config = region_config
        self.thread_streamer = None
        self.thread_counter = None

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
        streamer = Streamer(self.url_stream, 1, 20)
        predictor = Predictor(
            counter, (x_min, y_min, x_max, y_max), line_in, line_out, polygon, verbose=1
        )

        self.thread_streamer = threading.Thread(target=streamer.run, daemon=True)
        self.thread_counter = threading.Thread(target=predictor.run, daemon=True)

        self.thread_streamer.start()
        self.thread_counter.start()

        print(f"✅ Stream started for {self.url_stream}")


# store running jobs globally
JOBS = {}


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

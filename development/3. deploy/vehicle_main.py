import threading
from ultralytics import YOLO
from ultralytics.solutions import ObjectCounter

from vehicle_streamer import VehicleStreamer
from vehicle_counter import VehicleCounter


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
    vehicle_streamer = VehicleStreamer(url, 1, 20)
    vehicle_counter = VehicleCounter(
        counter,
        (x_min, y_min, x_max, y_max),
        line_in,
        line_out,
        polygon,
        # False,
        verbose=1,
    )

    t1 = threading.Thread(target=vehicle_streamer.run)
    t2 = threading.Thread(target=vehicle_counter.run)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("✅ Program exited gracefully")

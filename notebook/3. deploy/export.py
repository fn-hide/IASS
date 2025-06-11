from ultralytics import YOLO


def export():
    import os

    print(os.getcwd())
    model = YOLO("./asset/result/yolo11n_100_best.pt")
    model.export(format="engine")


if __name__ == "__main__":
    export()

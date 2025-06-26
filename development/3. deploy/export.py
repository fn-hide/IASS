import os
from ultralytics import YOLO


def export(path: str, format: str, name: str, **kwargs):
    dirpath, basename = os.path.split(path)
    filename, ext = os.path.splitext(basename)

    dstpath = os.path.join(dirpath, f"{filename}.{format}")
    tmppath = os.path.join(dirpath, f"{filename}_temp.{format}")
    newpath = os.path.join(dirpath, f"{filename}_{name}.{format}")

    if os.path.exists(dstpath):
        os.rename(dstpath, tmppath)

    model = YOLO(path)
    model.export(format=format, **kwargs)

    os.rename(dstpath, newpath)
    if os.path.exists(tmppath):
        os.rename(tmppath, dstpath)


if __name__ == "__main__":
    # export(
    #     "./asset/result/data_yolo11m_100/detect/train/weights/best.pt",
    #     "onnx",
    #     "cpu_nms",
    #     device="cpu",
    #     nms=True,
    # )

    model = YOLO("./asset/result/data_yolo11m_100/detect/train/weights/best.pt")
    model.export(format="tflite")

"""Inference with CPU not Google Coral"""

import os
import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics import solutions


def crop_and_mask_image(
    img: np.ndarray,
    x_min: int,
    y_min: int,
    x_max: int,
    y_max: int,
    polygon: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    # crop top-bottom
    img = img[y_min:y_max, x_min:x_max].copy()

    # fill black left-right
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [polygon], color=255)
    img = cv2.bitwise_and(img, img, mask=mask)
    # img = np.ascontiguousarray(img)

    return img


def stack_image(
    stack1: np.ndarray,
    stack2: np.ndarray,
    x_min: int,
    y_min: int,
    x_max: int,
    y_max: int,
) -> np.ndarray:
    # restore image by merge with original image
    mask = cv2.cvtColor(stack2, cv2.COLOR_BGR2GRAY) > 0
    mask_3ch = np.stack([mask] * 3, axis=-1)
    stack1[y_min:y_max, x_min:x_max][mask_3ch] = stack2[mask_3ch]
    return stack1


def adjust_xy(polygon: np.ndarray, x_min: int, y_min: int) -> np.ndarray:
    return np.array([(max(0, x - x_min), max(0, y - y_min)) for (x, y) in polygon])


def adjust_site_region(
    polygon: list | np.ndarray,
    line_in: list | np.ndarray | None = None,
    line_out: list | np.ndarray | None = None,
) -> tuple[
    tuple[int, int, int, int],
    np.ndarray,
    np.ndarray | None,
    np.ndarray | None,
]:
    # type validity check
    if isinstance(polygon, list):
        polygon = np.array(polygon)
    if isinstance(line_in, list):
        line_in = np.array(line_in)
    if isinstance(line_out, list):
        line_out = np.array(line_out)

    # shape validity check
    if polygon.shape != (4, 2):
        raise ValueError(f"{polygon.shape} is invalid shape for `polygon`")

    # get min and max pixel value from polygon
    x_min, y_min = np.min(polygon, axis=0).tolist()
    x_max, y_max = np.max(polygon, axis=0).tolist()
    # adjust original polygon and line towards crop image
    polygon = adjust_xy(polygon=polygon, x_min=x_min, y_min=y_min)
    if line_in is not None:
        if line_in.shape != (2, 2):
            raise ValueError(f"{line_in.shape} is invalid shape for `line_in`")
        line_in = adjust_xy(line_in, x_min=x_min, y_min=y_min)
    if line_out is not None:
        if line_out.shape != (2, 2):
            raise ValueError(f"{line_out.shape} is invalid shape for `line_out`")
        line_out = adjust_xy(line_out, x_min=x_min, y_min=y_min)
    return (x_min, y_min, x_max, y_max), polygon, line_in, line_out


class Inference:
    def __init__(
        self,
        name_model: str,
        path_video: str,
        border_xy: tuple[int, int, int, int],
        line_in: np.ndarray,
        line_out: np.ndarray,
        polygon: np.ndarray,
        dir_model=None,
        dir_output=None,
    ):
        """
        Parameters
        ----------
        name_model : str
            should be a relative path from `export` into `model`, eg: "export_best_yolov8n/best_saved_model/yolov8n_full_integer_quant_edgetpu.tflite"
        """
        self.name_model = name_model
        self.path_video = path_video
        self.x_min, self.y_min, self.x_max, self.y_max = border_xy
        self.line_in = line_in
        self.line_out = line_out
        self.polygon = polygon
        self.dir_model = dir_model
        self.dir_output = dir_output

        # generate output name
        name_result = os.path.splitext(os.path.basename(self.path_video))[0] + ".avi"
        name_export = name_model.split("/")[0]
        name_model = os.path.split(self.name_model)[-1].replace(".", "_")
        name_result = f"{name_export}-{name_model}-{name_result}"

        self.path_model = (
            os.path.join(self.dir_model, self.name_model)
            if self.dir_model
            else self.name_model
        )
        self.path_output = (
            os.path.join(self.dir_output, name_result)
            if self.dir_output
            else name_result
        )

    def run(self):
        cap = cv2.VideoCapture(self.path_video)
        assert cap.isOpened(), "Error reading video file"
        w, h, fps = (
            int(cap.get(x))
            for x in (
                cv2.CAP_PROP_FRAME_WIDTH,
                cv2.CAP_PROP_FRAME_HEIGHT,
                cv2.CAP_PROP_FPS,
            )
        )
        video_writer = cv2.VideoWriter(
            self.path_output, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h)
        )

        model = YOLO(self.path_model)
        counter = solutions.ObjectCounter(
            show=False,
            region=self.line_out,
            model=model,
        )

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print(
                    "Video frame is empty or video processing has been successfully completed."
                )
                break

            im1 = frame.copy()
            im1 = crop_and_mask_image(
                im1, self.x_min, self.y_min, self.x_max, self.y_max, self.polygon
            )
            results = counter(im1)
            im1 = stack_image(
                frame,
                results.plot_im,
                self.x_min,
                self.y_min,
                self.x_max,
                self.y_max,
            )
            video_writer.write(im1)

        cap.release()
        video_writer.release()


if __name__ == "__main__":
    line_in = None
    line_out = [[148, 659], [1782, 662]]
    polygon = [[174, 900], [678, 161], [1294, 161], [1663, 915]]
    (x_min, y_min, x_max, y_max), polygon, line_in, line_out = adjust_site_region(
        polygon, line_in, line_out
    )

    inference = Inference(
        "export_best_yolov8n_openvino/best_openvino_model",
        "assets/delta.mp4",
        (x_min, y_min, x_max, y_max),
        line_in,
        line_out,
        polygon,
        dir_model="results",
        dir_output="results",
    )
    inference.run()

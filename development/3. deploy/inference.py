"""Inference with CPU not Google Coral"""

import os
import cv2
from ultralytics import YOLO
from ultralytics import solutions


class Inference:
    def __init__(
        self,
        name_model: str,
        path_video: str,
        region_points: list,
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
        self.region_points = region_points
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
            region=self.region_points,
            model=model,
        )

        while cap.isOpened():
            success, im0 = cap.read()
            if not success:
                print(
                    "Video frame is empty or video processing has been successfully completed."
                )
                break
            results = counter(im0)
            video_writer.write(results.plot_im)

        cap.release()
        video_writer.release()


if __name__ == "__main__":
    name_model = "export_best_yolov8n"
    format_model = "best.onnx"
    name_video = "jpo_embong_malang_01.mp4"
    name_result = os.path.splitext(name_video)[0] + ".avi"

    inference = Inference(
        "export_best_yolov8n_openvino/best_openvino_model",
        "assets/jpo_embong_malang_01.mp4",
        [[7, 1106], [3193, 1073]],
        dir_model="results",
        dir_output="results",
    )
    inference.run()

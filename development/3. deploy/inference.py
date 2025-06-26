from ultralytics import YOLO


# print(get_cfg())

# Load a model
model = YOLO(
    "C:/users/eats/projects/IASS/asset/result/export_yolov8n/yolov8n_saved_model/yolov8n_full_integer_quant_edgetpu.tflite"
)  # Load a official model or custom model
print(model.names)

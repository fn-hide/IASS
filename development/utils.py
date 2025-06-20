import cv2 as cv
import numpy as np


def get_coordinates(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        print(f"({x}, {y})", end=", ")


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
    cv.fillPoly(mask, [polygon], color=255)
    img = cv.bitwise_and(img, img, mask=mask)
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
    mask = cv.cvtColor(stack2, cv.COLOR_BGR2GRAY) > 0
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

import cv2 as cv
import numpy as np


def get_coordinates(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        print(f"({x}, {y})", end=", ")


def crop_and_mask_image(
    img: np.ndarray,
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    polygon: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    # crop top-bottom
    img = img[y_min:y_max, x_min:x_max]

    # fill black left-right
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv.fillPoly(mask, [polygon], color=255)
    img = cv.bitwise_and(img, img, mask=mask)
    img = np.ascontiguousarray(img)

    return img


def stack_image(
    stack1: np.ndarray,
    stack2: np.ndarray,
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
) -> np.ndarray:
    # restore image by merge with original image
    mask = cv.cvtColor(stack2, cv.COLOR_BGR2GRAY) > 0
    mask_3ch = np.stack([mask] * 3, axis=-1)
    stack1[y_min:y_max, x_min:x_max][mask_3ch] = stack2[mask_3ch]
    return stack1

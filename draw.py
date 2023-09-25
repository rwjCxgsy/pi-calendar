import cv2
from typing import List

def draw_text(cv: cv2, lines: List[str], x, y, size, bold):
    ((single_width, single_height), base_height) = cv.getTextSize(lines[0][0])
    for i, line in enumerate(lines):
        
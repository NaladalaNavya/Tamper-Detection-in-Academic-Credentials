# Compare with known templates using OpenCV
"""Template matching is a method in computer vision where you search for a small image (template) 
inside a larger image (sourceThis is useful for checking if a certificate was tampered with
 — for example, if the layout, logos, or text boxes are missing or moved."""

import cv2
import numpy as np

def match_template(source_path, template_path, threshold=0.8):
    source = cv2.imread(source_path)
    template = cv2.imread(template_path)

    gray_src = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    gray_tpl = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_src, gray_tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    matched = False
    for pt in zip(*loc[::-1]):
        cv2.rectangle(source, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 0, 255), 2)
        matched = True

    return matched, source

# For parsing and visualizing annotation boxes
import cv2

def draw_boxes(image_path, annotations, output_path=None):
    image = cv2.imread(image_path)
    for ann in annotations:
        x, y, w, h = ann['x'], ann['y'], ann['width'], ann['height']
        cls = ann['class']

        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 1)

    if output_path:
        cv2.imwrite(output_path, image)
    return image

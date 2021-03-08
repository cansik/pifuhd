import glob
import os
import cv2
import argparse
import json
import numpy as np


def read_txt_file(file):
    with open(file) as f:
        return f.read()


def read_json(file):
    with open(file) as f:
        return json.load(f)


def bounding_box(xs, ys):
    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)

    w = x_max - x_min
    h = y_max - y_min

    return x_min + (w / 2), y_min + (h / 2), w, h


def resize_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="sample_images", help="The directory containing the images")
    parser.add_argument("--size", default=720, type=int, help="Display size (image will be resized) -1 for no resize")
    args = parser.parse_args()

    for img_file in glob.glob(os.path.join(args.dir, "*.png")):
        annotation_file = os.path.splitext(img_file)[0] + "_keypoints.json"

        # check if a annotation is available
        if not os.path.exists(annotation_file):
            continue

        # load img and txt
        frame = cv2.imread(img_file, 1)
        annotation = read_json(annotation_file)

        # extract keypoints of the body
        selected_data = annotation["people"][0]
        keypoints = np.array(selected_data['pose_keypoints_2d']).reshape(-1, 3)
        xs = keypoints[:, 0]
        ys = keypoints[:, 1]

        x, y, w, h = bounding_box(xs, ys)
        x = x - (w / 2)
        y = y - (h / 2)

        # annotate bounding box
        p1 = (int(x), int(y))
        p2 = (int(x + w), int(y + h))
        color = (255, 0, 255)
        cv2.rectangle(frame, p1, p2, color, 2)

        # annotate keypoints
        for kp in keypoints:
            cv2.circle(frame, (int(kp[0]), int(kp[1])), 10, (255, 255, 0), 2)

        if args.size > 0:
            frame = resize_with_aspect_ratio(frame, width=args.size)

        cv2.imshow('Preview', frame)

        key = cv2.waitKey()
        if key == 27:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()

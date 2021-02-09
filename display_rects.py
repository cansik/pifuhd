import glob
import os
import cv2
import argparse


def read_txt_file(file):
    with open(file) as f:
        return f.read()


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
    parser.add_argument("--size", default=1280, type=int, help="Display size (image will be resized) -1 for no resize")
    args = parser.parse_args()

    for img_file in glob.glob(os.path.join(args.dir, "*.png")):
        txt_file = os.path.splitext(img_file)[0] + "_rect.txt"

        # check if a txt is available
        if not os.path.exists(txt_file):
            continue

        # load img and txt
        frame = cv2.imread(img_file, 1)
        tokens = read_txt_file(txt_file).split("\n")[0].split(" ")
        rx, ry, rw, rh = tuple(map(lambda t: int(t.strip()), tokens))

        w = rw
        h = rh
        x = rx
        y = ry

        # annotate
        p1 = (x, y)
        p2 = (x + w, y + h)
        color = (255, 0, 0)

        cv2.rectangle(frame, p1, p2, color, 2)

        if args.size > 0:
            frame = resize_with_aspect_ratio(frame, width=args.size)

        cv2.imshow('Preview', frame)

        key = cv2.waitKey()
        if key == 27:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()

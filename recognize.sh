# create rect
cd lightweight-human-pose-estimation.pytorch
python create_rect.py --image bowie.png

# Warning: all images with the corresponding rectangle files under -i will be processed.
python -m apps.simple_test -r 256 --use_rect -i sample_images
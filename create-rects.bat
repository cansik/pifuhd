@echo off
echo "creating rects..."

pushd lightweight-human-pose-estimation.pytorch
for /r %%f in (..\sample_images\*.png) do echo "processing %%f..." && python create_rect.py --image "%%f" 
popd

echo "done!"
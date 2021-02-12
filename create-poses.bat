@echo off
echo "creating poses..."

:: cd {0}; ./build/examples/openpose/openpose.bin --image_dir {1} --write_json {2} --render_pose 2 --face --face_render 2 --hand --hand_render 2".format(op_dir, input_path, out_json_path)

SET IMAGE_PATH="C:\Users\flori\git\ZHdK\pifuhd\sample_images"

pushd ..\openpose
bin\openpose.exe --image_dir %IMAGE_PATH% --write_json %IMAGE_PATH% --render_pose 2 --face --face_render 2 --hand --hand_render 2
popd

echo "done!"
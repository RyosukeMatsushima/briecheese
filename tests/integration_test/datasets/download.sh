#!bin/bash

# using datasets from here.
# https://vision.middlebury.edu/stereo/data/

wget https://vision.middlebury.edu/stereo/data/scenes2021/data/artroom1/im0.png
wget https://vision.middlebury.edu/stereo/data/scenes2021/data/artroom1/im1.png
wget https://vision.middlebury.edu/stereo/data/scenes2021/data/artroom1/calib.txt

sed -i 's/\ /,\ /g' ./calib.txt
sed -i 's/;//g' ./calib.txt
mv calib.txt calib.py

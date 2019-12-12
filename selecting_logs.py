import numpy as np
import cv2
from PIL import Image
from template_matching import *
import sys
import csv
import subprocess

if len(sys.argv) == 3:
    img_path = sys.argv[1]
    img_pathR = sys.argv[2]
elif len(sys.argv) == 2:
    a = int(sys.argv[1])
    img_path = "imgs/%d.png" % a
    img_pathR = "imgs2/%d.png" % a
else:
    img_path = "imgs/1.png"
    img_pathR = "imgs2/1.png"

temp_paths = []
for i in range(12):
    temp_paths.append("templates/template_%d.png" % i)
center = scale_invariant_template_matching(0, img_path, temp_paths)
center_R = scale_invariant_template_matching(0, img_pathR, temp_paths)

known_centers = []
centers_path = "centers.csv"
with open(centers_path,"r") as f:
    reader = csv.reader(f)
    for row in reader:
        known_centers.append(row)

known_centersR = []
centersR_path = "centersR.csv"
with open(centersR_path,"r") as f:
    reader = csv.reader(f)
    for row in reader:
        known_centersR.append(row)

centersR_path = "heights.csv"
with open(centersR_path,"r") as f:
    reader = csv.reader(f)
    h = next(reader)[0]
    hh = map(float, h.split())
    heights = list(hh)
#print(heights)
#print(known_centers)



euclid_distance = 10**10
index = 0
i = 0
h = 0
delta_x = (int(center[0]) - int(center_R[0]))
pic = 63.0 / (delta_x)
f = 720*256/1280
height = pic * f ## [mm]
x = (128 - int(center[0]))*pic
y = (128 - int(center[1]))*pic
#x = (128 - int(center[0]))
#y = (128 - int(center[1]))

for centerL, centerR, height_ in (zip(known_centers,known_centersR, heights)):
    #if i==a-1:
    #    i += 1
    #    continue
    #print(i)
    center_ = (int(centerL[0]), int(centerL[1]))
    delta_x_ = (int(centerL[0]) - int(centerR[0]))
    print(centerL, centerR)
    pic_ = 63.0 / (delta_x_)
    print("pic: ", pic, pic_)

    x_ = (128 - int(center_[0]))*pic_
    y_ = (128 - int(center_[1]))*pic_
    #x_ = (128 - int(center_[0]))
    #y_ = (128 - int(center_[1]))
    print('i,',i)
    print(center[0], center[1], center_[0], center_[1])
    print(x, y, x_, y_)
    print(pic, pic_)
    distance = (x - x_)**2 + (y - y_)**2 + (height - height_)**2
    #print(x, x_, y, y_, height, height_)
    if distance < euclid_distance:
        euclid_distance = distance
        index = i
        h = height_
    i+=1

print("detected center: ", center, center_R)
print("euclid distance: ", euclid_distance)
print("height: ", height, h)
print("index:",index+1, "centerL of that index:", known_centers[index])


f = open('execute_num.txt', 'w')
f.write(str(index+1))
f.close()
print("index:",index+1, "centerL of that index:", known_centers[index])

subprocess.call("scp execute_num.txt ur:/home/ohmura/prog/trackingUR/", shell=True)
#res = subprocess.call(command)
res = subprocess.call("ssh ur python /home/ohmura/prog/trackingUR/execute.py", shell=True)


'''
imgL_0,1,250cm
scp -r testlogs ur:~/prog/trackingUR
cp -r testlogs ../
ur/prog/trackingUR/
'''

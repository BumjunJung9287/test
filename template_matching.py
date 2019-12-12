import numpy
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import csv

#im = Image.open("circle.png")
#im = np.array(im, dtype=np.uint32)
#print(im.shape) # (62s31s4)
#for i in range(10):
#    print(im[i])

def tem_mat(img2, template, meth):
    w,h = template.shape[1], template.shape[0]
    img = img2.copy()
    method = eval(meth)

    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # if the mathod is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum. else maximum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
        val = min_val
        #print(min_val)
    else:
        val = max_val
        top_left = max_loc
        #print(max_val)
    bottom_right = (top_left[0] + w, top_left[1] + h)
    center = (top_left[0] + int(w/2), top_left[1] + int(h/2))
    #print(center)

    red_color = (0,0,0)
    img = cv2.line(img, center, center, red_color, 5)

    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    '''
    plt.subplot(121), plt.imshow(res)
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img)
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.subplot(121), plt.imshow(template)
    plt.title('template'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)

    plt.show()
    '''
    return top_left, w, h, val, center

def scale_invariant_template_matching(n, img_path, temp_paths):
    img = cv2.imread(img_path, -1)
    #img = img[110:,:,:]
    img = cv2.resize(img, dsize=(256,256))
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
    img2 = img.copy()
    templates = []
    for i in range(len(temp_paths)):
        templates.append(cv2.cvtColor(cv2.imread(temp_paths[i],-1), cv2.COLOR_RGBA2BGRA))

    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    e = 0.9

    val = 0
    e_num = 0
    for i in range(10):
        for template in templates:
            top_left_, w_, h_, val_, center_ = tem_mat(img2, template, methods[1])
            if val_>val:
                top_left = top_left_
                w = w_
                h = h_
                val = val_
                center = center_
                e_num = i

        a,b = img2.shape[0:2]
        img2 = cv2.resize(img2, dsize=(int(a/e), int(b/e)), interpolation=cv2.INTER_LINEAR)
        #print(img2.shape)

    top_left = int(top_left[0]*(e**e_num)), int(top_left[1]*(e**e_num))
    w = int(w*(e**e_num)); h = int(h*(e**e_num));
    center = int(center[0]*(e**e_num)), int(center[1]*(e**e_num))

    #print(center)
    red_color = (255,0,0,255)

    bottom_right = (top_left[0] + w, top_left[1] + h)
    center = (top_left[0] + int(w/2), top_left[1] + int(h/2))
    img = cv2.line(img, center, center, red_color, 5)
    print(center)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    '''
    plt.subplot(121)
    plt.imshow(img)
    plt.title('Detected Point %d' %n), plt.xticks([]), plt.yticks([])
    #plt.savefig("detectedimg%d"%n)
    plt.show()
    '''
    if n!=100:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
        cv2.imwrite("detectied_{}.png".format(n), img)

    return center
if __name__ == "__main__":
    temp_paths = []
    for i in range(12):
        temp_paths.append("templates/template_%d.png" % i)
    #temp_paths = ["template_1.png","template_2.png","template_3.png","template_4.png"]
    centers = []
    centersR = []
    heights = []
    #not_working = [5,10,11,13,14,16,22,23,31,34,38,43,44,52,54,56,61,62,71,75]
    #for i in not_working:
    for i in range(1,76):
        img_path = "imgs/%d.png" % i
        center = scale_invariant_template_matching(i,img_path, temp_paths)
        img_path = "imgs2/%d.png" % i
        centerR = scale_invariant_template_matching(i,img_path, temp_paths)
        centers.append(center)
        centersR.append(centerR)
        delta_x = (int(center[0]) - int(centerR[0]))
        pic = 63 / (delta_x)
        f = 720*256/1280
        height = pic * f
        x = (128 - int(center[0]))*pic
        y = (128 - int(center[0]))*pic
        heights.append(str(height))
        print(center,centerR,height)
    print(heights)

    center_path = "centers.csv"
    #for center in centers:
    with open(center_path,"w",newline="") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(centers)

    centerR_path = "centersR.csv"
    #for center in centers:
    with open(centerR_path,"w",newline="") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(centersR)

    height_path = "heights.csv"
    with open(height_path,"w",newline="") as f:
        csvwriter = csv.writer(f, delimiter=" ")
        csvwriter.writerow(heights)

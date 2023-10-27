import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import scipy

def find_in_frame(frame, template, method=cv2.TM_CCOEFF):

    img = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    img2 = img.copy()
    
    # template = cv2.imread(to_loc, cv2.IMREAD_GRAYSCALE)
    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = template.shape[::-1]

    
    res = cv2.matchTemplate(img, template, method)
    # print(res)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    return top_left, bottom_right

def MSE(img1, img2):
    squared_diff = (img1 -img2) ** 2
    summed = np.sum(squared_diff)
    num_pix = img1.shape[0] * img1.shape[1]
    err = summed / num_pix
    return err

def create_circle_icon(path, resize=None):
    
    img = cv2.imread(path)
    hh, ww = img.shape[:2]
    hh2 = hh // 2
    ww2 = ww // 2

    # define circles
    radius = hh2
    yc = hh2
    xc = ww2

    # draw filled circle in white on black background as mask
    mask = np.zeros_like(img)
    mask = cv2.circle(mask, (xc,yc), radius, (255,255,255), -1)

    # apply mask to image
    result = cv2.bitwise_and(img, mask)
    if resize is not None:
        result = cv2.resize(result, dsize=resize)

    return result

def minimap_detection(img, champs_to_detect):

    if isinstance(img, str):
        img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows = gray.shape[0]
     
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 32, param1=100, param2=30,
        minRadius=18, maxRadius=25)
     
    if circles is None:
        return {}
    
    circles = np.uint16(np.around(circles))
    average_radius = math.ceil(circles[:, :, -1].mean())

    icons = {}
    for champ in champs_to_detect:
        icons[champ] = create_circle_icon(f"data/assets/league_of_legends/{champ}.png", 
                                          resize=(average_radius*2, average_radius*2))
        
    dists = []
    
    for i in circles[0, :]:
    
        center = (i[0], i[1])
        radius = i[2] 

        mask = np.zeros_like(img)
        mask = cv2.circle(mask, center, radius + 1, (255,255,255), -1)
        
        result = cv2.bitwise_and(img, mask)
        crop = result[center[1] - radius:center[1] + radius,
                center[0] - radius:center[0] + radius, :]

        resized_crop = cv2.resize(crop, (average_radius*2, average_radius*2))

        current_dist = []
        for k, v in icons.items():
            current_dist.append(MSE(resized_crop, v))
        
        dists.append(current_dist)

    assignement = scipy.optimize.linear_sum_assignment(dists)
    
    result = {}
    for row, col in zip(assignement[0], assignement[1]):
    
        current_circle = circles[0, row, :]
            
        champ_name = list(icons.keys())[col]
        
        result[champ_name] = (current_circle[0], current_circle[1])
        # img = cv2.putText(img, champ_name, (current_circle[0], current_circle[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  
        #     (255, 0, 0) , 1, cv2.LINE_AA, False)  

    return result
import argparse
import matplotlib.pyplot as plt

import cv2
import random
import numpy as np

def crop_frame(frame, coords):

    cropped_frame = frame

    if len(coords) == 4:

        x1, y1, x2, y2 = coords
        cropped_frame = frame[x1:x2, y1:y2, :]
        
    return cropped_frame

def display_single_frame(filepath, img_idx=1000):

    cap = cv2.VideoCapture(filepath)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
 

    count = 0
    while(cap.isOpened()):
    
        ret, frame = cap.read()
        if ret:
            count += 1
            if count == img_idx:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                plt.imshow(img)
                plt.show()

                dummy_coords = [902, 2024, 1413, 2536]
                cropped_frame = crop_frame(img, dummy_coords)
                
                plt.imshow(cropped_frame)
                plt.show()

                cap.release()
        

def save_frame_sample(filepath, output_path, crop=False):

    cap = cv2.VideoCapture(filepath)

    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    
    # Read until video is completed

    count = 0
    while(cap.isOpened()):
    
        ret, frame = cap.read()
        if ret:
            if count % 10 == 0:
                print(f"Saving frame {count} ...")
                if crop:
                    dummy_coords = [902, 2024, 1413, 2536]
                    frame = crop_frame(frame, dummy_coords)

                output_name = f"{output_path}_{count}.jpeg" 
                cv2.imwrite(output_name, frame)
            count += 1

        else:
            break

    cap.release()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("filepath")
    parser.add_argument("box_coords", nargs="+", type=int)

    args = parser.parse_args()

    print(args.filepath)
    print(args.box_coords)

    display_single_frame(args.filepath, img_idx=100)
    save_frame_sample(args.filepath, "data/imgs_lol/minimap_custom", True)


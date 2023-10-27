import argparse

from src.matching.loc import find_in_frame, minimap_detection
from src.utils import crop_frame

import cv2
import matplotlib.pyplot as plt

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("frame")
    parser.add_argument("--video")

    args = parser.parse_args()

    # red_team = ["garen", "xin_zhao", "kassadin", "miss_fortune", "lux"]
    # blue_team = ["jax", "sejuani", "vladimir", "kaisa", "rakan"]
    
    # final_img = cv2.imread(args.frame)
    # for champ in red_team:
        
    #     img = cv2.imread(f"data/assets/league_of_legends/{champ}.png", cv2.IMREAD_GRAYSCALE)
    #     img_resize = cv2.resize(img, (40, 40))

    #     top_left, _ = find_in_frame(args.frame, img_resize)
    #     print(top_left)
        
    #     final_img = cv2.putText(final_img, champ, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5,  
    #              (0, 0, 255) , 1, cv2.LINE_AA, False)

    # for champ in blue_team:
        
    #     img = cv2.imread(f"data/assets/league_of_legends/{champ}.png", cv2.IMREAD_GRAYSCALE)
    #     img_resize = cv2.resize(img, (40, 40))

        
    #     top_left, _ = find_in_frame(args.frame, img_resize)
        
    #     final_img = cv2.putText(final_img, champ, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5,  
    #              (255, 0, 0) , 1, cv2.LINE_AA, False)  

    # plt.imshow(final_img[:, :,  (2, 1, 0)])
    # plt.show()

    # ===========================================================================================
    
    red_team = ["garen", "xin_zhao", "kassadin", "miss_fortune", "lux"]
    blue_team = ["jax", "sejuani", "vladimir", "kaisa", "rakan"]
    if args.video is None:
        
        result = minimap_detection(args.frame, red_team + blue_team)

        img = cv2.imread(args.frame)
        for k, v in result.items():
            img = cv2.putText(img, k, v, cv2.FONT_HERSHEY_SIMPLEX, 0.5,  
            (0, 255, 0) , 1, cv2.LINE_AA, False)     

        plt.imshow(img[:, :, (2, 1, 0)])
        plt.show()

    else:
        cap = cv2.VideoCapture(args.video)

        if (cap.isOpened()== False): 
            print("Error opening video stream or file")
        
        # Read until video is completed

        count = 0
        while(cap.isOpened()):
        
            ret, frame = cap.read()
        
            if ret == True:
                dummy_coords = [902, 2024, 1413, 2536]
                frame = crop_frame(frame, dummy_coords)
                result = minimap_detection(frame, red_team + blue_team)
                for k, v in result.items():
                    frame = cv2.putText(frame, k, v, cv2.FONT_HERSHEY_SIMPLEX, 0.5,  
                    (0, 255, 0) , 1, cv2.LINE_AA, False)
                
                cv2.imwrite(f"data/results/{count}.jpeg", frame)
                count += 1
                # plt.imshow(frame)
                # plt.show()

            # Break the loop
            else:
                break 
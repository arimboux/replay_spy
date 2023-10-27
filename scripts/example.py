import argparse

from src.matching.loc import find_in_frame

import cv2
import matplotlib.pyplot as plt

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("frame")

    args = parser.parse_args()

    red_team = ["garen", "xin_zhao", "kassadin", "miss_fortune", "lux"]
    blue_team = ["jax", "sejuani", "vladimir", "kaisa", "rakan"]
    
    final_img = cv2.imread(args.frame)
    for champ in red_team:
        
        img = cv2.imread(f"data/assets/league_of_legends/{champ}.png", cv2.IMREAD_GRAYSCALE)
        img_resize = cv2.resize(img, (20, 20))

        top_left, _ = find_in_frame(args.frame, img_resize, cv2.TM_CCORR)
        
        img = cv2.putText(final_img, champ, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5,  
                 (0, 0, 255) , 1, cv2.LINE_AA, False) 

    plt.imshow(img[:, :,  (2, 1, 0)])
    plt.show()
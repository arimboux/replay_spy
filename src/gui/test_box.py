import json
import sys
import matplotlib.pyplot as plt
import cv2

filename = sys.argv[1]

with open("test.json", "r") as f:
    annots = json.load(f)

img = cv2.imread(filename)
for ann in annots["annotations"]:
    x1, y1 = ann["coords"][:2]
    x2 = x1 + ann["coords"][2]
    y2 = y1 + ann["coords"][3]
    
    img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

plt.imshow(img[:, :, (2, 1, 0)])
plt.show()
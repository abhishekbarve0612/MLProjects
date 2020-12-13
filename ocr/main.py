import numpy
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread("img.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print(pytesseract.image_to_string(img))

image_height, image_width, dim = img.shape
boxes = pytesseract.image_to_boxes(img)
for box in boxes.splitlines():
    print(box)
    box = box.split(' ')
    print(box)
    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
    cv2.rectangle(img, (x, image_height - y), (w, image_height - h), (32, 231, 20), 2)
    cv2.putText(img, box[0], (x, image_height - y + 30), cv2.FONT_HERSHEY_DUPLEX, 1, (153, 32, 32), 2)


cv2.imshow('Characters Detected', img)

img = cv2.imread("img.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

image_height, image_width, dim = img.shape
boxes = pytesseract.image_to_data(img)

for a, b in enumerate(boxes.splitlines()):
    # print(b)
    if a != 0:
        b = b.split()
        if len(b) == 12:
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            cv2.putText(img, b[-1], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (33, 22, 55), 2)
            cv2.rectangle(img, (x,y), (x+w, y+h), (66, 44, 22), 2)

cv2.imshow('Words Detected', img)

img = cv2.imread("img.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

image_height, image_width, dim = img.shape
conf = r'--oem 3 --psm 6 outputbase digits'
boxes = pytesseract.image_to_boxes(img, config=conf)

for b in boxes.splitlines():
    # print(b)
    b = b.split(' ')
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.putText(img,b[0],(x,image_height- y+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (93, 22, 155), 2)
    cv2.rectangle(img, (x, image_height - y), (w, image_height - h), (75, 25, 25), 2)


cv2.imshow("Digits Detected", img)
cv2.waitKey(0)

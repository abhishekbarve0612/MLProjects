import cv2

threshold = 0.45

capture = cv2.VideoCapture(0)

capture.set(3, 500)
capture.set(4, 500)

classNames = []
classFile = 'coco.names'

with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

print(classNames)

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weights = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weights, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObject(img):
    classIds, confs, bbox = net.detect(
        img, confThreshold=threshold, nmsThreshold=0.2)
    print(classIds, bbox)

    if len(classIds) > 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(12, 44, 3), thickness=2)
            cv2.putText(img, classNames[classId-1].upper(), (box[0] + 10,
                                                             box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (11, 77, 21), 2)
            cv2.putText(img, str(round(confidence*100, 2)),
                        (box[0] + 200, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (11, 77, 21), 2)
    return img


if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    capture.set(3, 500)
    capture.set(4, 500)
    while True:
        success, img = capture.read()
        result = getObject(img)
        cv2.imshow("Output", img)
        cv2.waitKey(1)

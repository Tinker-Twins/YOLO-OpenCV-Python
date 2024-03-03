import cv2 as cv
import numpy as np

# Load YOLO Model
net = cv.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Load Classes
with open("coco.names", 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Configuration
layer_name = net.getLayerNames()
output_layer = [layer_name[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Load Image
img = cv.imread("image.jpg")
img = cv.resize(img, None, fx=0.2, fy=0.2)
height, width, channel = img.shape

# Detect Objects
blob = cv.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layer)

# Display Object Detection Information
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w/2)
            y = int(center_y - h/2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
indices = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
font = cv.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indices:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = np.round(confidences[i]*100, 2)
        size = w*h
        print('Class: {} \t Confidence: {} % \t Size: {} px²'.format(label, confidence, size))
        color = colors[i]
        cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv.putText(img, label, (x, y + 30), font, 3, color, 3)
cv.imshow("Object Detection", img)
cv.waitKey(0)
cv.destroyAllWindows() # Wait For 'ESC' Key
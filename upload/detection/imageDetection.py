from sys import path

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from django.conf.global_settings import MEDIA_ROOT

from nutrition.settings import MEDIA_URL
def imageDetection(filename):

    net = cv2.dnn.readNet('upload/detection/yolov3.weights', 'upload/detection/yolov3.cfg')
    # yolo weights, cfg파일을 views.py와 같은 경로에 위치
    # gulim.ttc 글꼴 파일도 views.py와 같은 경로에 위치
    classes = ['백미밥', '배추김치', '계란프라이', '스팸', '라면', '조미김']
    layer_names = net.getLayerNames()
    output_layers = ['yolo_16','yolo_23']
    colors = np.random.uniform(0,255, size = (len(classes), 3))

    # img : 업로드 된 이미지 파일 이름
    # 이미지 로드 시키는 코드 필요
    # print(filename)
    img = cv2.imread(filename)
    # img = cv2.resize(src, None, fx=0.5, fy=0.5)
    height, width, channels = img.shape

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    font = ImageFont.truetype("upload/detection/NanumSquare_acR.ttf", 10)  # 한글 출력을 위해
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    class_list = []
    x_list = []
    y_list = []

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            class_list.append(label)
            color = colors[(i % 6)]
            x_list.append(x)  # 각각 x,y를 list형식으로 저장
            y_list.append(y)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)  # 우선 검출된 객체를 box bounding

    img = Image.fromarray(img)  # img배열을 PIL이 처리가능하게 변환
    draw = ImageDraw.Draw(img)

    for i in range(len(x_list)):
        color = colors[(i % 6)]
        color_int = [int(j) for j in color]
        draw.text((x_list[i], y_list[i] - 12), str(class_list[i]), font=font, fill=tuple(color_int))  # text를 출력
    #
    # img = np.array(img)  # 파일형식 변환
    #
    # cv2.imwrite("result.jpg", img)

    # class_list : 검출된 객체 이름 list => DB 저장 코드 필요?
    # 최종 img를 html로 넘기는 코드 필요
    print(class_list)
    return class_list



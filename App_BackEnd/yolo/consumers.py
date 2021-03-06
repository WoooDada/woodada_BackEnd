import json
from channels.generic.websocket import WebsocketConsumer
import base64
import cv2
import torch
import numpy as np
from django.utils import timezone
from api.models import User
from study.models import Daily_1m_content


global total_play
global total_con

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def isOverlapped(list1, list2):
    #list=(a,b,c,d)
    if list1[0] < list2[2] and list1[2] > list2[0] and list1[1] < list2[3] and list1[3] > list2[1] :
        return True
    else :
        return False


def base64_file(data, name=None):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    str_decoded = base64.b64decode(imgstr)

    jpg_as_np = np.frombuffer(str_decoded, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)

    return img


class sendConsumer(WebsocketConsumer):
    def connect(self):
       # print("connected")

        global total_play
        global total_con

        total_con=0
        total_play=0

        self.accept()


    def disconnect(self, code):
        # print("disconnected")
        pass



    def receive(self, text_data):

        global total_play, total_con

        data = json.loads(text_data)
        message = data['message']
      #  nickname = data['nickname']

        img = base64_file(message, name='yolo_picture')             #base64로 이미지 decode하기

        w=img.shape[0]
        h=img.shape[1]

        #모델에 적용
        model = torch.hub.load('yolov5', 'custom', path='yolo/static/best.pt', source='local',force_reload=True)
        results = model(img)

        results_array = results.pandas().xyxy[0].to_json(orient="records")      #결과값 json변환


        results_array = results_array.replace("'","\"")     #'을 "로 치환해야 json으로 변환 가능함
        results_array = json.loads(results_array)       #string을 json(dict)형식으로 변환

        class_array = []
        for result in results_array:
            get_confidence = result['confidence']
            get_class = result['name']

            if get_confidence >= 0.1:
                class_array.append(get_class)



        if 'face' in class_array:
            type = 'P'
            # message = 'yes face'
        else:
            if ('book' in class_array) or ('tablet' in class_array):
                if 'phone' in class_array:
                    type = 'C'
                #   message = 'handphone'

                else:
                    if 'handonly' in class_array:
                        type = 'C'
                    #   #     message = 'handonly'
                    elif 'pen' in class_array:
                        type = 'C'

                    else:
                        type = 'P'
                    #       message='none'

            else:
                type = 'P'
                # message = 'no face no desk'

        # client로 데이터 보내기기
        self.send(
            text_data=json.dumps({
                'type': type
            })
        )


        def receive(self, text_data):
            now = timezone.now()
            hour = now.hour
            minute = now.minute
            time = str(hour) + ":" + str(minute)



        if type == 'C':
            total_con += 1
        elif type == 'P':
            total_play += 1

        if total_con + total_play == 20:
            now = timezone.now()
            hour = now.hour
            minute = now.minute

            if hour < 10:
                hour = "0" + str(hour)
            else:
                hour = str(hour)
            if minute < 10:
                minute = "0" + str(minute)
            else:
                minute = str(minute)

            time = hour + ":" + minute

            uid = data['uid']
            user = User.objects.get(uid=uid)

            Daily_1m_content.objects.create(uid=user, type=type, time=time).save()

            total_con = 0
            total_play = 0




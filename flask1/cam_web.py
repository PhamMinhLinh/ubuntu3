import os
import cv2
import numpy as np
import tensorflow as tf
import sys
from flask import Flask, render_template, Response
import time
import pygame
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from threading import Timer, Thread, Event
import sound
font = cv2.FONT_HERSHEY_SIMPLEX
app = Flask(__name__)
# set path cho thu muc lam viec
sys.path.append("..")
# pygame.init()
# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

cred = credentials.Certificate("filedatabase.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://argon-radius-377619-default-rtdb.firebaseio.com/'})
ref = db.reference('random_number')
# def on_update(event):
#     print('New value:', event.data)
# ref.listen(on_update)
# Name of the directory containing the object detection module we're using
MODEL_NAME = 'model'
# Grab path to current working directory
CWD_PATH = os.getcwd()
# Đường dẫn đến tệp .pb chứa mô hình được sử dụng để phát hiện đối tượng.
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, '100K-steps.pb')
# Đường dẫn đến tệp nhãn
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, 'label_map.pbtxt')
# Number of classes the object detector can identify
NUM_CLASSES = 3
# PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
# # Path to label map file
# PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')
## Tải bản đồ nhãn.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)
# Tải mô hình Tensorflow vào bộ nhớ.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    sess = tf.compat.v1.Session(graph=detection_graph)
# Xác định các tensor đầu vào và đầu ra (tức là dữ liệu) cho trình phân loại phát hiện đối tượng
# Tensor đầu vào là hình ảnh
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# Tensor đầu ra là các hộp phát hiện, điểm số và các lớp
# Mỗi hộp đại diện cho một phần của hình ảnh nơi phát hiện một đối tượng cụ thể
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# Mỗi điểm thể hiện mức độ tự tin cho từng đối tượng.
# Điểm được hiển thị trên hình ảnh kết quả, cùng với nhãn lớp.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
# Số lượng đối tượng được phát hiện
num_detections = detection_graph.get_tensor_by_name('num_detections:0')
n1 = []


class XTimer(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
    def run(self):
        while not self.stopped.wait(20):
            count = len(n1) #100
            print(count)
            if 90 <count <= 200:
                print('=====================NGA===================')
                #sound.am1()
                rand_num =  100
                #query_example()
            elif count < 90:
                print('BTH@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                rand_num = 10
            n1.clear()
            def on_update(event):
                print('New value:', event.data)

            ref.listen(on_update)
            ref.set(rand_num)
            rand_num= 0


def gen():
    video = cv2.VideoCapture(0)
    _= video.set(3, 1280)
    _= video.set(4, 720)
    # Read until video is completed
    while (video.isOpened()):
        ret, frame = video.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)
        # Thực hiện phát hiện thực tế bằng cách chạy mô hình với hình ảnh làm đầu vào
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})
        # Draw the results of the detection (aka 'visulaize the results')
        # Vẽ kết quả phát hiện (hay còn gọi là 'hiển thị kết quả')
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=5,
            min_score_thresh=0.75,
        )
        chinhxac = scores[0][0]
        if category_index[classes[0][0]]['name'] == "head":
            if chinhxac >= 0.75:
                box = np.squeeze(boxes)
                for boxes in range(len(boxes)):
                    ymin = box[boxes, 0] * 720
                    if (ymin > 200):
                        # ham dem so fame dau duoi line
                        if category_index[classes[0][0]]['id'] == 2:
                            id1 = category_index[classes[0][0]]['id'] == 2
                            n1.append(id1)
                            print(len(n1))
                            # b = len(n1)
                            # if b>90:
                            #  rand_num = 100
                            #  ref.set(rand_num)
                            #  print ('nga ơ dưới')

        elif category_index[classes[0][0]]['name'] == "fall":
            if chinhxac >= 0.8:
                cv2.putText(frame, "nga", (380, 20), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                print('co dau hieu nga')
               #sound.am1()
                rand_num = 100
                ref.set(rand_num)

        cv2.line(frame, (0, 200), (1920,200), (255, 0, 255), 4)
        # đang sử dụng Motion JPEG, nhưng OpenCV mặc định chụp ảnh thô
        # vì vậy phải mã hóa nó thành JPEG để hiển thị chính xác sau do chuyen thanh dang bye
        frame1 = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: frame/jpeg\r\n\r\n' + frame1 + b'\r\n')
        # time.sleep(0.1)
        key = cv2.waitKey(20)
        if key == 27:
            break




# web tạo 1 phần điều khiển của trang web /
@app.route('/')
def index():
    """Video streaming home page."""
    stopFlag = Event()
    thread = XTimer(stopFlag)
    thread.start()
    return render_template('index.html')  # , canh_bao=status_cam)
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False)
import cv2
# import socket
import numpy
import argparse
import airsim
from MAVProxy.modules.lib import multiproc
from MAVProxy.modules.lib import mp_image
import time

if __name__ == '__main__':
    multiproc.freeze_support()
    
    ap = argparse.ArgumentParser()
    ap.add_argument("--delay",type=float,default=0.5)
    ap.add_argument("--port", type=int, default=19721)
    ap.add_argument("--title", type=str, default='FPV Camera Feed')
    args = ap.parse_args()
    viewer = mp_image.MPImage(title=args.title, width=320, height=240, auto_size=True)

    client = airsim.MultirotorClient()
    lastt=time.time()
    dt_list = []
    j = 1
    while True:


        apiRequest = client.simGetImages([airsim.ImageRequest("0",airsim.ImageType.Scene)])
        apiSingle = apiRequest[0]


        encodedImage = apiSingle.image_data_uint8
        timestamp = apiSingle.time_stamp
        now = time.time()
        dt = now - lastt

        # Groundtruth timestamp, x,y,z,q1,q2,q3,q4
        groundtruth_pos = apiSingle.camera_position
        


        if encodedImage is None:
            continue

        img = cv2.imdecode(numpy.fromstring(encodedImage, dtype=numpy.uint8),cv2.IMREAD_COLOR)
        viewer.set_image(img, bgr=True)
        time.sleep(args.delay)
        lastt = now

        dt_list.append(dt)

        if j%100 == 0:
            print(groundtruth_pos)
            avg_dt = round(1/(float(sum(dt_list))/len(dt_list)),3)
            print("Frame-rate: " + str(avg_dt) + " fps")

        j = j + 1

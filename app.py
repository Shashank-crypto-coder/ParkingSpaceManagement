import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import StreamingResponse
import cv2
import pickle
import cvzone
import numpy as np


import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory="templates")


# @app.get("/")
# async def root():
#    return {"message": "hello world"}

# @app.get("/")
# def read_root():
#     with open("templates/base.html", 'r') as file:
#         content = file.read()
#     return HTMLResponse(content=content)


# @app.get("/video")
# async def get_video():
#     return FileResponse("static/Video_1.mp4", media_type="video/mp4")
# @app.get("/video")
# async def get_video():
#     return FileResponse("static/Video_2.mp4", media_type="video/mp4")

# To run locally
# if __name__ == '__main__':
#    uvicorn.run(app, host='0.0.0.0', port=8000)

def management(video_file,pickle_file):
    cap = cv2.VideoCapture(video_file)
    if (cap.isOpened()== False):
	    print("Error opening video file")
    with open(pickle_file,'rb') as p:
        position_list = pickle.load(p)
    width,height = 33,15

    return gen_frames(cap,position_list,width,height)

# cap = cv2.VideoCapture("static/Video_1.mp4")
# if (cap.isOpened()== False):
# 	print("Error opening video file")


# with open("CarParkingPosition",'rb') as p:
#     position_list = pickle.load(p)

# width,height = 33,15

def check(processed_image,img,position_list,width,height):
    counter = 0
    tracker_list=[]
    pos_tracker=[]
    for pos in position_list:
        x,y = pos    
        
        img_crop=processed_image[y:y+height,x:x+width]
        count = cv2.countNonZero(img_crop)
        cvzone.putTextRect(img, str(count), (x,y+height-5), scale=0.5, thickness=1, offset=0)
        
        if count<80:
            color = (0,255,0)
            thickness = 5
            counter += 1
            pos_tracker.append(position_list.index(pos))
            #print(pos_tracker)
            #print(position_list.index(pos))
        else:
            color = (0,0,255)
            thickness = 2 
            
        cv2.rectangle(img,pos,(pos[0]+width, pos[1]+height ), color ,2)
        
    tracker_list.append(pos_tracker)
    cvzone.putTextRect(img, f'Free : {counter} / {len(position_list)}', (280,310), scale=0.8, thickness=1, offset=20, colorR=(100,100,10))
    return tracker_list,counter

def gen_frames(cap,position_list,width,height):
    while(cap.isOpened()):
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        ret,img = cap.read()
        gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur_img = cv2.GaussianBlur(gray_img,(3,3),1)
        threshold_img = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY_INV, 25,16)
        median_img = cv2.medianBlur(threshold_img, 5)
        kernel = np.ones((3,3), np.int8)

        dilated_img = cv2.dilate(median_img, kernel , iterations=1)
            
        tracker_list,counter = check(dilated_img,img,position_list,width,height)
        
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'COntent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        
@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/video_feed_1')
def video_feed_1():
    return StreamingResponse(management("static/Video_1.mp4","CarParkingPosition"), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/video_feed_2')
def video_feed_2():
    return StreamingResponse(management("static/Video_1.mp4","CarParkingPosition"), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)
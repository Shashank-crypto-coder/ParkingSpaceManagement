import numpy as np
import cv2
import pickle
import pandas as pd
from datetime import datetime



# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('static/Video_1.mp4')

with open("CarParkingPosition",'rb') as p:
    position_list = pickle.load(p)
    
k = len(position_list)

col = ['slot' + str(i) for i in range(k)]
col.insert(0, "Timestamp")
df=pd.DataFrame(columns= col)
#df.loc[len(df)] = [1,2]
#print(df.head())



width,height = 33,15

def check(processed_image):
    counter = 0
    tracker_list=[]
    pos_tracker=[]
    for pos in position_list:
        x,y = pos
        
        
        
        img_crop=processed_image[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),img_crop)
        count = cv2.countNonZero(img_crop)
        
        #cvzone.putTextRect(img, str(count), (x,y+height-5), scale=0.5, thickness=1, offset=0)
        
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
            
        #cv2.rectangle(img,pos,(pos[0]+width, pos[1]+height ), color ,2)
    #print(pos_tracker)
        
    tracker_list.append(pos_tracker)
    arr = np.ones(k)
    for i in pos_tracker:
        arr[i] = 0
    #print('/'*50)
    #print(arr)
    print(counter)
    
    arr1 = arr.tolist()
    #arr1 = map(str, arr1)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    arr1.insert(0,current_time)
    df.loc[len(df)] = arr1
    #df.loc[len(df)-1]["timestamp"] = current_time
    #print(df.loc[len(df)-1]["timestamp"])
    #print('*'*50)
        
    #cvzone.putTextRect(img, f'Free : {counter} / {len(position_list)}', (280,310), scale=0.8, thickness=1, offset=20, colorR=(100,100,10))
    return tracker_list,counter
    
    

# Check if camera opened successfully
if (cap.isOpened()== False):
	print("Error opening video file")

# Read until video is completed
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
        
    tracker_list,counter = check(dilated_img)
    
    #for pos in position_list:
        #cv2.rectangle(img,pos,(pos[0]+width, pos[1]+height ), (255,0,255),2)
    
    
    #if ret == True:
        #cv2.imshow('Frame', img)
        #cv2.imshow('Gray_Frame', gray_img)
        #cv2.imshow('Blur_Frame', blur_img)
        #cv2.imshow('Threshold_Frame', threshold_img)
        #cv2.imshow('Median_Blur_Frame', median_img)
        #cv2.imshow('Dilated_Frame', dilated_img)
        #if cv2.waitKey(25) & 0xFF == ord('q'):
            #break
    if ret == False:
        break
    #
     #   cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    
	
		
    

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
#%%
#print(tracker_list)


#%%
#print(df.head())
#print(df.shape)
#%%


# df.to_csv("ParkingFlow.csv")


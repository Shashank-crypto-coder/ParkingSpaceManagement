import cv2
import pickle



width,height = 33,15

try:
    with open("CarParkingPosition",'wb') as p:
        position_list = pickle.load(p)
except:
    position_list=[]
    

def mouseClick(events , x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        position_list.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(position_list):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                position_list.pop(i)

    with open("CarParkingPosition",'wb') as p:
        pickle.dump(position_list, p)
        
while True:
    
    # cv2.rectangle(img,(60,168),(155,215),(255,0,255),2)
    img = cv2.imread("frame2.jpg")
    for pos in position_list:
        cv2.rectangle(img,pos,(pos[0]+width, pos[1]+height ), (255,0,255),2)
    #cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty("img",100,100)
        
    cv2.imshow("img",img)
    cv2.setMouseCallback("img", mouseClick)
    cv2.waitKey(1)

cv2.destroyAllWindows()


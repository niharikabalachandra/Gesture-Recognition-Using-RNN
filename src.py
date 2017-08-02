import sys, os
sys.path.insert(0, "../lib")
sys.path.insert(0, "../lib/x64")
import Leap
import time
import pandas as pd
import numpy as np
from PIL import Image

leftHand=[]
rightHand=[]
count=502
left_count=238
right_count=259
count_free=0
previous_time=0
frame_count=0
class SimpleListener(Leap.Listener):
    
    def on_connect(self, controller):
        print "Connected"
        
        
        
    def on_frame(self, controller):
        global count,left_count,right_count, count_free,previous_time,frame_count
        
        frame=controller.frame()
        hand=frame.hands
        lFlag=False
        rFlag=False
        
        if not hand.is_empty:
            for h in hand:
                if h.is_left:
                    leftHand=h
                    lFlag=True
                elif h.is_right:
                    rightHand=h
                    rFlag=True
            if lFlag and rFlag:
                pass
            
            elif lFlag:
                
                
# Recording Left Gesture

                if (leftHand.palm_normal.roll* Leap.RAD_TO_DEG<=35 and leftHand.palm_normal.roll* Leap.RAD_TO_DEG>0) and len(leftHand.fingers.extended())==1: 
                    print "Hand Detected for Left"
                    time.sleep(1.5)
                    print "Record now"
                    time.sleep(0.5)
                    frame=controller.frame()
                    lefthand=frame.hands[0]
                    current_time=frame.timestamp
                    time_delta=current_time-previous_time

                    data_left=[[] for _ in range(12)]
                    # Record only if frame rate during gesture is low
                    if time_delta>5e6 and time_delta<1e9:
                        for i in range(59,-1,-1):
                            data_left[0].append(count)
                            data_left[1].append(round(controller.frame(i).hand(lefthand.id).stabilized_palm_position[0],4))
                            data_left[2].append(round(controller.frame(i).hand(lefthand.id).stabilized_palm_position[1],4))
                            data_left[3].append(round(controller.frame(i).hand(lefthand.id).stabilized_palm_position[2],4))
                            data_left[4].append(round(controller.frame(i).hand(lefthand.id).stabilized_palm_position[0],4)-round(controller.frame(59).hand(lefthand.id).stabilized_palm_position[0],4))
                            data_left[5].append(round(controller.frame(i).hand(lefthand.id).stabilized_palm_position[1],4)-round(controller.frame(59).hand(lefthand.id).stabilized_palm_position[1],4))
                            data_left[6].append(round(controller.frame(i).hand(lefthand.id).stabilized_palm_position[2],4)-round(controller.frame(59).hand(lefthand.id).stabilized_palm_position[2],4))                    
                            data_left[7].append(round(controller.frame(i).hand(lefthand.id).palm_normal.roll,4))
                            data_left[8].append(round(controller.frame(i).hand(lefthand.id).direction.yaw,4))
                            data_left[9].append(round(controller.frame(i).hand(lefthand.id).direction.pitch,4))
                            data_left[10].append(int(rFlag))
                            data_left[11].append(1)
    
                        df_left=pd.DataFrame(data=data_left)
                        df_left=df_left.transpose()  
                        df_left.to_csv("./CSV/%s.csv"%(str(count)),sep=',',index=False, header=False)
                        count+=1
                        left_count+=1
                        print "Swipe Left Gesture Recorded %s" %(str(left_count))
                    else:
                        print "Try Again"
                    time.sleep(3)
                    print "Ready"
                    time.sleep(1)
                    previous_time=current_time

                    
# Recording Right Gesture

                if ((rightHand.palm_normal.roll* Leap.RAD_TO_DEG>=-35 and rightHand.palm_normal.roll* Leap.RAD_TO_DEG<0) and (len(rightHand.fingers.extended())==1)): 
                    print "Hand Detected for Swipe Right"
                    time.sleep(1.5)
                    print "Record now"
                    time.sleep(0.5)
                    frame=controller.frame()
                    righthand=frame.hands[0]
                    current_time=frame.timestamp
                    time_delta=current_time-previous_time
                    data_right=[[] for _ in range(12)]
                    # Record only if frame rate during gesture is low
                    if time_delta>5e6 and time_delta<1e9:
                        for i in range(59,-1,-1):
                            data_right[0].append(count)
                            data_right[1].append(round(controller.frame(i).hand(righthand.id).stabilized_palm_position[0],4))
                            data_right[2].append(round(controller.frame(i).hand(righthand.id).stabilized_palm_position[1],4))
                            data_right[3].append(round(controller.frame(i).hand(righthand.id).stabilized_palm_position[2],4))
                            data_right[4].append(round(controller.frame(i).hand(righthand.id).stabilized_palm_position[0],4)-round(controller.frame(59).hand(righthand.id).stabilized_palm_position[0],4))
                            data_right[5].append(round(controller.frame(i).hand(righthand.id).stabilized_palm_position[1],4)-round(controller.frame(59).hand(righthand.id).stabilized_palm_position[1],4))
                            data_right[6].append(round(controller.frame(i).hand(righthand.id).stabilized_palm_position[2],4)-round(controller.frame(59).hand(righthand.id).stabilized_palm_position[2],4))                    
                            data_right[7].append(round(controller.frame(i).hand(righthand.id).palm_normal.roll,4))
                            data_right[8].append(round(controller.frame(i).hand(righthand.id).direction.yaw,4))
                            data_right[9].append(round(controller.frame(i).hand(righthand.id).direction.pitch,4))
                            data_right[10].append(int(rFlag))
                            data_right[11].append(0)

                        df_right=pd.DataFrame(data=data_right)
                        df_right=df_right.transpose()
                        df_right.to_csv("./CSV/%s.csv"%(str(count)),sep=',',index=False, header=False)
                        count+=1
                        right_count+=1
                        print "Swipe Right Gesture Recorded %s" %(str(right_count)) 
                    else:
                        print "Try Again"
                    time.sleep(3)
                    print "Ready"
                    time.sleep(1)
                    previous_time=current_time

            
        else:
            pass
            
          

def main():
    listener = SimpleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    # Run infinitely until Enter is pressed
    print "Hit Enter to quit!"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
    
if __name__ == "__main__":
    main()

    

    
    
    
    

    

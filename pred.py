import numpy as np
import pandas as pd
from keras.models import load_model
from keras.utils import np_utils
import time
import sys
sys.path.insert(0, "../lib")
sys.path.insert(0, "../lib/x64")
import Leap
import tensorflow as tf
import os

leftHand=[]
rightHand=[]
previous_time=0

#Load the model
model=load_model('model_test.h5')
print "Model Loaded"

gesture=["Swipe Right","Swipe Left"]
audio=["aplay right.wav","aplay left.wav"]
graph=tf.get_default_graph()

class SimpleListener(Leap.Listener):
    
    def on_connect(self, controller):
        print "Connected"
              
    def on_frame(self, controller):
        global model, graph,previous_time, gesture, audio
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

                print "Hand Detected"
                time.sleep(1.5)
                print "Record now"
                time.sleep(0.5)
                frame=controller.frame()
                lefthand=frame.hands[0]
                current_time=frame.timestamp
                time_delta=current_time-previous_time
                data_left=[[] for _ in range(12)]
                if time_delta>4e6 and time_delta<1e9:
                    for i in range(59,-1,-1):
                        data_left[0].append(0)
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
            
                    x=df_left.iloc[:,1:11].values
                    with graph.as_default():
                        y_pred=model.predict(np.reshape(x,(1,x.shape[0],x.shape[1])))
                    pred=np.argmax(y_pred)
                    # Eliminate the False Postives
                    if (y_pred[0][1] or y_pred[0][0])>=0.3:
                        print gesture[pred]
                        os.system(audio[pred])
                    else:
                        print "try again"
                else:
                    print "Try Again"
          
                time.sleep(3)
                print "Ready"
                time.sleep(1)
                previous_time=current_time
                    
                        

            elif rFlag:

    
                print "Hand Detected"
                time.sleep(1.5)
                print "Record now"
                time.sleep(0.5)
                
                frame=controller.frame()
                righthand=frame.hands[0]
                current_time=frame.timestamp
                time_delta=current_time-previous_time
                data_right=[[] for _ in range(12)]
                if time_delta>5e6 and time_delta<1e9:
                    for i in range(59,-1,-1):
                        data_right[0].append(0)
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
            
                    x = df_right.iloc[:, 1:11].values
                    with graph.as_default():
                        y_pred=model.predict(np.reshape(x,(1,x.shape[0],x.shape[1])))
                    pred=np.argmax(y_pred)
                    # Eliminate the False Postives
                    if (y_pred[0][0] or y_pred[0][1])>=0.3:
                        print gesture[pred]
                        os.system(audio[pred])
                    else:
                        print "try again"
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

    print "Hit Enter to quit!"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
    
if __name__ == "__main__":
    main()

#!/usr/bin/env python

import rospy
import numpy as np
import math 
import scipy as sp
import rosnode
import time
from comunicating_robots.msg import Position, Input
from costants import *
from scipy.integrate import odeint, ode


def callback(data, pub):
    global con_iniziali
    if not hasattr(callback, "int_time"):
       callback.int_time = start_t #tempo d'integrazione
    if not hasattr(callback, "last_state"):
       callback.last_state = con_iniziali #ultimo stato
    sim_rate = rospy.Rate(rate)
    sim_rate.sleep()
    input_msg = Input()
    input_msg.v = data.v
    input_msg.w = data.w
    msg = Position()
    if input_msg.v == v_des:
       rospy.loginfo('Arrivati a destinazione v='+str(input_msg.v)+' w='+str(input_msg.w))
    if input_msg.v ==v_safe:
       print("Robot troppo vicini")
    #divido il tempo in step e calcolo il nuovo stato risolvendo le equazioni differenziali
    t_points = np.arange(callback.int_time, callback.int_time+delta, step)
    state = odeint(odeSys, callback.last_state, t_points, args=(input_msg.v, input_msg.w))
    callback.int_time+=delta
    #pubblico il messaggio
    msg.x = state[len(state)-1][0]
    msg.y = state[len(state)-1][1]
    msg.theta = state[len(state)-1][2]
    #aggiorno le condizioni iniziali
    callback.last_state[0] = msg.x
    callback.last_state[1] = msg.y
    callback.last_state[2] = msg.theta
    pub.publish(msg)
    rospy.loginfo('t: '+str(callback.int_time)+' x='+str(msg.x)+' y='+str(msg.y)+' theta='+str(msg.theta)+' v='+str(input_msg.v)+' w='+str(input_msg.w))

#calcolo derivate di stato
def odeSys(last_state, t, v, w):
    # compute state derivatives
    xd = v*np.cos(last_state[2]) 
    yd = v*np.sin(last_state[2])
    thetad = w
    #return the state derivatives
    return [xd, yd, thetad]    

def sendInitialState(pub, con_iniziali):
    msg = Position()	
    msg.x = con_iniziali[0]
    msg.y = con_iniziali[1]
    msg.theta = math.radians(con_iniziali[2])
    rospy.loginfo('Stato iniziale: x='+str(msg.x)+' y='+str(msg.y)+' theta='+str(msg.theta))
    pub.publish(msg)

if __name__ == '__main__':
    try:
    #dichiaro il nodo al master e definisco il topic a cui mando messaggi di tipo Position (x,y,theta)
      name_space = rospy.get_namespace()
      con_iniziali = state0[name_space]
      robot_name = rospy.get_param(name_space)
      pub = rospy.Publisher('/stateTopic_'+robot_name, Position, queue_size=0)
      rospy.init_node('simulator_'+robot_name, anonymous=False)
      print rospy.get_name() 
      sim_rate = rospy.Rate(rate)
      #aspetto finche' si colleghi il controllore e mando lo stato iniziale
      time.sleep(3)
      sendInitialState(pub, con_iniziali)
      sub = rospy.Subscriber('/inputTopic_'+robot_name, Input, callback, (pub))
      rospy.spin()
    except rospy.ROSInterruptException:
        print "errore"

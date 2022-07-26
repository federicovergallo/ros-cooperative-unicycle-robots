#!/usr/bin/env python

import rospy
import numpy as np
from costants import *
from comunicating_robots.msg import PdesPosition, Position
#calcolo distanza 
def distanza(x1,y1,x2,y2):
    return (np.sqrt(np.power(x2-x1,2)+np.power(y2-y1,2))) 

def callback_follower(data):
    if not hasattr(callback_follower, "p_follower"):
       callback_follower.p_follower = PdesPosition()
    callback_follower.p_follower = data

def callback(data, robot_name):
    if not hasattr(callback, "pub"):
       callback.pub = rospy.Publisher('/pdesTopic_'+robot_name, PdesPosition, queue_size=0)
    if not hasattr(callback, "p_leader"):
       callback.p_leader = Position()
    callback.p_leader = data

    pdes_rate=rospy.Rate(rate)
    pdes_rate.sleep()

    msg = PdesPosition()
    while not hasattr(callback_follower, "p_follower"):
       pdes_rate.sleep()

    if distanza(callback_follower.p_follower.x, callback_follower.p_follower.y, callback.p_leader.x, callback.p_leader.y) < safe_dist:
       msg.safe_flag = True
    else:
       msg.safe_flag = False

    msg.x = callback.p_leader.x
    msg.y = callback.p_leader.y

    while callback.pub.get_num_connections() == 0:
       pdes_rate.sleep()

    rospy.loginfo('Posizione desiderata di '+robot_name+' x='+str(data.x)+' y='+str(data.y))
    callback.pub.publish(msg)

def publish_leader(robot_name):
   pdes_rate=rospy.Rate(rate)
   if not hasattr(publish_leader, "pub"):
       publish_leader.pub = rospy.Publisher('/pdesTopic_'+robot_name, PdesPosition, queue_size=0)
   while publish_leader.pub.get_num_connections() == 0:
      pdes_rate.sleep()
   msg = PdesPosition()
   msg.x = xdes
   msg.y = ydes
   msg.safe_flag = False
   publish_leader.pub.publish(msg)

if __name__ == '__main__':
    name_space = rospy.get_namespace()
    robot_name = rospy.get_param(name_space)
    rospy.init_node('pdes_comunicator_'+robot_name, anonymous=False)
    rospy.loginfo(rospy.get_name())
    if robot_name == leader_name:
       publish_leader(robot_name)
    else:
       sub = rospy.Subscriber('/stateTopic_'+leader_name, Position, callback,(robot_name))
       sub1 = rospy.Subscriber('/stateTopic_'+robot_name, Position, callback_follower)
    rospy.spin()


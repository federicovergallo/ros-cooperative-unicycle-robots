# ROS Architecture for Cooperative Unicycle Robot

This repo contains my bachelor thesis in Theory of Systems (Teoria dei Sistemi) from the course given at Università del Salento in a.y. 2016-2017 by prof. Notarstefano. 

The thesis aimed at the development of a ROS architecture to simulate the behave of a certain number of unicycle robots controlled in a Leader - Follower scenario, i.e. to a Leader robot is given a desired position and computes its trajectory to reach that position, meanwhile its instantaneous position is sent to a number of Followers robot that integrates their trajectory to follow the Leader.

In the `docs/` section you can find my thesis (in Italian, sorry!) for more theoretical details.

I'll update the repo to make it more reproducible, but at the moment I can say that the requirements are:

 1. Ubuntu 16.04 (sorry it was the 2016!)
 2. ROS Catkin 
 3. Python 3.6

The plotted simulation result is the following:




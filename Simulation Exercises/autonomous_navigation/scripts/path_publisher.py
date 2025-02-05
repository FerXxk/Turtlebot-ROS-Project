#!/usr/bin/python3
# This Python file uses the following encoding: utf-8

import sys
import math
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path


if __name__ == '__main__':
    
    # Create the path publisher
    path_publisher = rospy.Publisher('path', Path, queue_size=10)
    rospy.init_node('path_publisher', anonymous=False)  
    seq = 0

    # Read path from the Param Server
    goals = sorted(rospy.get_param('path').items())

    # Fill the path message
    path = Path()
    path.header.frame_id = rospy.get_param("~path_frame", default="odom")
    seq_goals = 0
    for i in goals:
        pose = PoseStamped()
        pose.header.frame_id = path.header.frame_id
        pose.header.seq = seq_goals
        seq_goals += 1
        pose.pose.position.x = i[1]['x']
        pose.pose.position.y = i[1]['y']
        pose.pose.position.z = 0
        path.poses.append(pose)
        rospy.loginfo("Added point %f, %f", pose.pose.position.x, pose.pose.position.y)

    # Send the path each second
    r = rospy.Rate(1) # 1Hz
    while not rospy.is_shutdown():
        path.header.stamp = rospy.Time.now()
        path.header.seq = seq
        path_publisher.publish(path)
        seq = seq + 1
        r.sleep()

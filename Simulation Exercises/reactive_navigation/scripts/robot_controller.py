#!/usr/bin/python3
# This Python file uses the following encoding: utf-8

import math
import rospy
import tf
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

class TurtlebotController():
    
    def __init__(self, rate):
        
        # Read parameters
        self.goal_tol = 0.15
        
        self.rate = rate # Hz  (1/Hz = secs)
        
        # Initialize internal data 
        self.goal = PoseStamped()
        self.goal_received = False

        # Subscribers / publishers
        self.tf_listener = tf.TransformListener()

        self.cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        rospy.Subscriber("move_base_simple/goal", PoseStamped, self.goalCallback)
      
        rospy.loginfo("TurtlebotController started")
        

    def shutdown(self):
        # Stop turtlebot
        rospy.loginfo("Stop TurtleBot")
        # A default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
        # Sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)


    def goalCallback(self,goal):
        rospy.loginfo("Goal received! x: %.2f, y:%.2f", goal.pose.position.x, goal.pose.position.y)
        self.goal = goal  
        self.goal_received = True


    def command(self):

        # Check if we already received data
        if(self.goal_received == False):
            rospy.loginfo("Goal not received. Waiting...")
            return

        # Check if the final goal has been reached
        if(self.goalReached()==True):
            rospy.loginfo("GOAL REACHED!!! Stopping!")
            self.publish(0.0, 0.0)
            self.goal_received = False
            return
        
        #######################################################################################################
        # Check for collisions                                                                                #
        # Implement control law                                                                               #
        # Note: You could transform next goal to local robot coordinates to compute control law more easily   #
        # Note: You should saturate the maximum angular and linear robot velocities                           #
        #######################################################################################################
            
        # Publish velocity command
        self.publish(linear,angular)
        return False


    def goalReached(self):
        # Return True if the FINAL goal was reached, False otherwise

        if self.goal_received:
            pose_transformed = PoseStamped()

            # Update the goal timestamp to avoid issues with TF transform
            self.goal.header.stamp = rospy.Time()

            try:
                pose_transformed = self.tf_listener.transformPose('base_footprint', self.goal)
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                rospy.loginfo("Problem TF")
                return False

            goal_distance = math.sqrt(pose_transformed.pose.position.x ** 2 + pose_transformed.pose.position.y ** 2)
            if(goal_distance < self.goal_tol):
                return True

        return False

    
    def publish(self, lin_vel, ang_vel):
        # Twist is a datatype for velocity
        move_cmd = Twist()
        # Copy the forward velocity
        move_cmd.linear.x = lin_vel
        # Copy the angular velocity
        move_cmd.angular.z = ang_vel
        rospy.loginfo("Commanding lv: %.2f, av: %.2f", lin_vel, ang_vel)
        self.cmd_vel_pub.publish(move_cmd)


if __name__ == '__main__':
    
    # Initiliaze
    rospy.init_node('TurtlebotController', anonymous=False)

    # Tell user how to stop TurtleBot
    rospy.loginfo("To stop TurtleBot CTRL + C")

    rate = 10 # Frecuency (Hz) for commanding the robot
    robot = TurtlebotController(rate)
        
    # What function to call when you CTRL + C    
    rospy.on_shutdown(robot.shutdown)
        
    # TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
    r = rospy.Rate(rate)
        
    # As long as you haven't CTRL + C keeping doing...
    while not (rospy.is_shutdown()):
        
	    # Publish the velocity
        robot.command()

        # Wait for 0.1 seconds (10 HZ) and publish again
        r.sleep()

        

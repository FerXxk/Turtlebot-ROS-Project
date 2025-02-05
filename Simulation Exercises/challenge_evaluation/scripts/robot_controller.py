#!/usr/bin/python3
# This Python file uses the following encoding: utf-8

import math
import rospy
import tf
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Path


class TurtlebotController():
    
    def __init__(self, rate):
        
        # Read parameters
        self.goal_tol = 0.15
        self.max_lin_vel = rospy.get_param('~max_linear_velocity')
        self.max_ang_vel = rospy.get_param('~max_angular_velocity')
        
        self.rate = rate # Hz  (1/Hz = secs)
        self.angular_ant=0.5
        self.permanencia=True
        # Initialize internal data 
        self.goal = PoseStamped()
        self.goal_received = False
        self.goal_reached = True
        self.i=0

        # Subscribers / publishers
        self.tf_listener = tf.TransformListener()

        self.cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        rospy.Subscriber("move_base_simple/goal", PoseStamped, self.goalCallback) # We subscribe to coordinates 
        #rospy.Subscriber('path', Path,self.goalCallback)
        rospy.Subscriber("/scan", LaserScan, self.scanCallback)  # We subscribe to the LiDAR
        rospy.loginfo("TurtlebotController started")  
        

    def shutdown(self):
        # Stop turtlebot
        rospy.loginfo("Stop TurtleBot")
        # A default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
        # Sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

    
    def scanCallback(self,scan_data):
        # Update the minimum obstacle distance
        self.scan_data=scan_data


    def goalCallback(self,goal):
        rospy.loginfo("Goal received! x: %.2f, y:%.2f", goal.pose.position.x, goal.pose.position.y)
        self.goal = goal  
        self.goal_received = True



    def command(self):

        # Check if we already received data
        if(self.goal_received==False):
            rospy.loginfo("Goal not received. Waiting...")
            return

        # Check if the final goal has been reached
        if(self.goalReached()==True):
            rospy.loginfo("GOAL REACHED!!! Stopping!")
            self.publish(0.0, 0.0)
            self.goal_received = False
            return
        
        longitud=len(self.scan_data.ranges)
        self.min_dist_izq=100000 # Default values to update
        self.min_dist_der=100000
        self.min_dist_cen=100000

        for i in range(longitud):
            if i<=45: # We limit the FOV of the LiDAR to 90º
                if(self.min_dist_izq>self.scan_data.ranges[i]):
                    self.min_dist_izq=self.scan_data.ranges[i] # If the distance is minor, we update it.

                if(self.min_dist_cen>self.scan_data.ranges[i]):
                    self.min_dist_cen=self.scan_data.ranges[i]

            if i>=315:
                if(self.min_dist_der>self.scan_data.ranges[i]):  # We update the distances in three directions
                    self.min_dist_der=self.scan_data.ranges[i]

                if(self.min_dist_cen>self.scan_data.ranges[i]):
                    self.min_dist_cen=self.scan_data.ranges[i]

        
        self.goal_transformada=PoseStamped()
        
        self.goal.header.stamp=rospy.Time()
        self.goal_transformada=self.tf_listener.transformPose('base_footprint',self.goal) # We transform the global goal to the local reference of the robot


        goal_x = self.goal_transformada.pose.position.x  
        goal_y = self.goal_transformada.pose.position.y
        
        distance_to_goal = math.sqrt(goal_x**2 + goal_y**2) # We calculate the distance from the robot to the goal
        angle_to_goal = math.atan2(goal_y, goal_x) # We calculate the angle from the robot to the goal


        if(self.min_dist_cen<0.3):  # If the obstacle is too close:
            linear=0.0 # it stops going forward
            if(self.permanencia==True):
                self.permanencia=False
                if(self.min_dist_izq>self.min_dist_der): # The robot rotates in the opposite direction of the obstacle 
                    angular=self.max_ang_vel
                    self.angular_ant=angular
                else:
                    angular=-self.max_ang_vel
                    self.angular_ant=angular
            else:
                angular=self.angular_ant # If both directions are equally close to the obstacle, it rotates arbitrarily


        else:
            self.permanencia=True # If there isn't any obstacle close the robot goes forward and turning to the goal at the same time
            linear = min(self.max_lin_vel, distance_to_goal) # We saturate the speed
            angular = max(-self.max_ang_vel, min(self.max_ang_vel, angle_to_goal)) # We saturate the angle


        # Some messages to keep the user informated
        rospy.loginfo("Min range: %.2f",self.min_dist_cen)
        rospy.loginfo("Angulo a objetivo: %.2f",angle_to_goal)
        rospy.loginfo("Coordenadas locales  x:%.2f y:%.2f",self.goal_transformada.pose.position.x,self.goal_transformada.pose.position.y)

            
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
            if(goal_distance < self.goal_tol): # When the robot is closely enough to the goal, it is considered reached
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
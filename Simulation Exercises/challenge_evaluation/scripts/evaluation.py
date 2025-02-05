#!/usr/bin/python3
# This Python file uses the following encoding: utf-8

# This script is used for generating the statistics that will be used in
# the evaluation of the robotics challenge

import sys
import math
import rospy
import tf

from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray

class Evaluation:
    def __init__(self):
       
        rospy.loginfo("Starting Evaluation node...")
        self.listener = tf.TransformListener()
            
        self.base_frame = rospy.get_param('~base_frame', default='base_link')
        self.global_frame = rospy.get_param('~global_frame', default='map')
        
        self.output_file = rospy.get_param('~output_file', default='metrics.txt')
        self.max_lin_vel = rospy.get_param('~max_lin_vel', default=0.25)
        self.max_ang_vel = rospy.get_param('~max_ang_vel', default=1.2)
        self.goal_gap = rospy.get_param('~goal_tolerance', default=0.15) 
        self.min_collision = rospy.get_param('~min_collision_dist', default=0.1)
        
        # Get the robot pose in global frame
        self.has_transform = False
        while not(self.has_transform):
            self.init_x, self.init_y = self.getTransform()
            self.px = self.init_x
            self.py = self.init_y
        rospy.loginfo("Evaluation: got robot position! init_x = %f init_y=%f", self.init_x, self.init_y)

        self.metrics = self.Metrics(self.output_file)
        self.hist_dist_to_obs = []

        # Read the goals from the param server
        goals = sorted(rospy.get_param('/goals').items())
        self.goals_queue = []
        t = rospy.Time.now()
        for i in goals:
            rospy.loginfo("Reading goal x: %.2f, y: %.2f", i[1]['x'], i[1]['y'])
            pose = PoseStamped()
            pose.header.frame_id = self.global_frame
            pose.header.stamp = t
            #pose.header.seq = 0
            pose.pose.position.x = float(i[1]['x'])
            pose.pose.position.y = float(i[1]['y'])
            pose.pose.position.z = 0
            pose.pose.orientation.w = 1.0
            self.goals_queue.append(pose)

        # Generate visualization markers for goals
        markers = self.generate_visualization_goals()
        self.flag_markers = MarkerArray()
        
        # Take the first goal
        self.current_goal = self.goals_queue.pop(0)
        self.goal_sent = False
        self.time_limit = 200.0 # 200 seconds = 3 min 20 seg
        self.count = 0

        rospy.loginfo("Before publishers and subscribers....")
        self.goal_pub = rospy.Publisher("move_base_simple/goal", PoseStamped, queue_size=10)
        self.marker_pub = rospy.Publisher("goal_markers", MarkerArray, queue_size=10)
        self.flag_pub = rospy.Publisher("flag_markers", MarkerArray, queue_size=10)
        rospy.Subscriber("scan", LaserScan, self.scan_callback, queue_size=1)
        rospy.Subscriber("cmd_vel", Twist, self.cmd_vel_callback, queue_size=1)

        # Wait for RViz to be subscribed to the markers before publishing
        rate = rospy.Rate(2)
        while self.marker_pub.get_num_connections() < 1:
            rospy.loginfo("Waiting for subscribers...")
            rate.sleep()
        rospy.loginfo("Publishing markers")
        self.marker_pub.publish(markers)
        self.init_time = rospy.Time.now()
        
        
    class Metrics:
        def __init__(self, output_file):
        
            self.goal_reached = False
            self.distance_traveled = 0.0
            self.elapsed_time = 0.0
            self.min_dist_to_obs = 100.0
            self.avg_dist_to_obs = 0.0
            self.collision_penalty = 0
            self.lin_vel_penalty = 0
            self.ang_vel_penalty = 0
            self.out_file = output_file

        def store_metrics(self):
            rospy.loginfo("Stopped Evaluation node. Generating metrics result file")
            try:
                with open(self.out_file,'w') as f:
                    f.write('Goals reached: %s\n'%(self.goal_reached))
                    f.write('Elapsed time: %f\n'%(float(self.elapsed_time)))
                    f.write('Traveled distance: %f\n'%(self.distance_traveled))
                    f.write('Min distance to obstacles: %f\n'%(self.min_dist_to_obs))
                    f.write('Avg distance to obstacles: %f\n'%(self.avg_dist_to_obs))
                    f.write('Collision penalties: %d\n'%(self.collision_penalty))
                    #f.write('Linear vel penalties: %d\n'%(self.lin_vel_penalty))
                    #f.write('Angular vel penalties: %d\n'%(self.ang_vel_penalty))
                rospy.loginfo('File exported successfully. Filename: %s', self.out_file)
            except OSError as e:
                rospy.logerr('Could not save output file. Error: %s', str(e))

              
    def scan_callback(self, data):
        #rospy.loginfo("scan received")
        m = min(data.ranges)
        self.hist_dist_to_obs.append(m)
        if(m < self.metrics.min_dist_to_obs):
            self.metrics.min_dist_to_obs = m
        if(m <= self.min_collision):
            rospy.logwarn('Collision penalty!!!')
            self.metrics.collision_penalty += 1
        

    def cmd_vel_callback(self, data):
        #rospy.loginfo("cmd_vel received")
        if abs(data.linear.x) > self.max_lin_vel:
            rospy.logwarn('Linear vel penalty!!!')
            self.metrics.lin_vel_penalty += 1
        if abs(data.angular.z) > self.max_ang_vel:
            rospy.logwarn('Angular vel penalty!!!')
            self.metrics.ang_vel_penalty += 1

    def getTransform(self):
        try:
            (t,r) = self.listener.lookupTransform(self.global_frame,self.base_frame, rospy.Time(0))
            self.has_transform = True
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            return (0,0)

        return (t[0], t[1])
        

    def generate_visualization_goals(self):    
        ma = MarkerArray()
        t = rospy.Time.now()
        for i, p in enumerate(self.goals_queue):
            m = Marker()
            m.header.frame_id = p.header.frame_id
            m.header.stamp = t
            m.ns = "goals"
            m.id = i
            m.type = Marker.CYLINDER
            m.action = Marker.ADD
            m.lifetime = rospy.Duration(0)
            m.pose.position.x = p.pose.position.x
            m.pose.position.y = p.pose.position.y
            m.pose.position.z = 0.01
            m.pose.orientation.w = 1.0
            m.scale.x = 0.16
            m.scale.y = 0.16
            m.scale.z = 0.01
            m.color.a = 1.0
            m.color.r = 0.0
            m.color.g = 1.0
            m.color.b = 0.0
            ma.markers.append(m)
        return ma


    def publish_flag(self, goal):
        t = rospy.Time.now()
        m = Marker()
        i = len(self.flag_markers.markers)
        # Update stamps
        for f in self.flag_markers.markers:
            f.header.stamp = t

        m.header.frame_id = goal.header.frame_id
        m.header.stamp = t
        m.ns = "goal_flags"
        m.id = i
        m.type = Marker.CYLINDER
        m.action = Marker.ADD
        m.lifetime = rospy.Duration(0)
        m.pose.position.x = goal.pose.position.x
        m.pose.position.y = goal.pose.position.y
        m.pose.position.z = 0.02
        m.pose.orientation.w = 1.0
        m.scale.x = 0.16
        m.scale.y = 0.16
        m.scale.z = 0.01
        m.color.a = 1.0
        m.color.r = 0.0
        m.color.g = 0.0
        m.color.b = 1.0
        self.flag_markers.markers.append(m)
        rospy.loginfo("Publishing goal reached flag!")
        self.flag_pub.publish(self.flag_markers)


    def update(self):
        self.count += 1
        gx = self.current_goal.pose.position.x
        gy = self.current_goal.pose.position.y

        # If no goal has been sent, send it!
        if self.goal_sent == False and self.goal_pub.get_num_connections() > 0:
            
            #self.current_goal.header.stamp = rospy.Time.now()
            self.goal_pub.publish(self.current_goal)
            rospy.loginfo("\n\t\tNAVIGATION GOAL x:%.2f, y:%.2f SENT!\n", gx, gy)
            self.goal_sent = True
    
        # Get the current robot position in the map
        cx,cy = self.getTransform()

        # Check the distance to the current goal
        dist_goal = math.sqrt( (cx-gx)**2 + (cy-gy)**2)
        
        # Compute the distance that the robot has moved
        self.metrics.distance_traveled += math.sqrt( (cx-self.px)**2 + (cy-self.py)**2)
        # Update the current position
        self.px = cx
        self.py = cy

        # Check that we do not exceed a time deadline
        tdiff = rospy.Time.now() - self.init_time
        ts = float(tdiff.secs+tdiff.nsecs*1e-9)

        if self.count > 10:
            rospy.loginfo("Metrics update: Traveled distance %f Time: %.2f Dist to goal: %f", self.metrics.distance_traveled, ts, dist_goal)
            self.count = 0
 
        if(ts >= self.time_limit):
            rospy.loginfo("TIME ELAPSED EXCEEDED THE TIME LIMIT OF %.1f SECONDS!!!", self.time_limit) 
            self.metrics.elapsed_time = ts
            self.metrics.avg_dist_to_obs = round((sum(self.hist_dist_to_obs) / len(self.hist_dist_to_obs)), 2)
            sys.exit()

        # Has the goal been reached?
        if dist_goal <= self.goal_gap:
            rospy.loginfo("Goal x: %.2f, y: %.2f reached!!! Elapsed time: %.2f\n", gx, gy, ts)
            self.publish_flag(self.current_goal)
            # Update goal if possible
            if len(self.goals_queue) > 0:
                self.current_goal = self.goals_queue.pop(0)
                self.current_goal.header.seq += 1
                self.goal_sent = False
            else:
                #All goals has been reached, finish the program
                tdiff = rospy.Time.now() - self.init_time
                self.metrics.elapsed_time = float(tdiff.secs+tdiff.nsecs*1e-9)
                self.metrics.goal_reached = True
                self.metrics.avg_dist_to_obs = round((sum(self.hist_dist_to_obs) / len(self.hist_dist_to_obs)), 2)
                rospy.loginfo("ALL THE GOALS REACHED!!! Storing metrics...")
                sys.exit()


    def shutdown(self):
        self.metrics.store_metrics()
 


if __name__ == '__main__':
    # initiliaze
    rospy.init_node('Evaluation', anonymous=False)

	# tell user how to stop TurtleBot
        
    rospy.loginfo("To stop the Evaluation node press CTRL + C")

    eval=Evaluation()
	# What function to call when you ctrl + c    
    rospy.on_shutdown(eval.shutdown)

    # Rate (Hz) to execute the loop
    r = rospy.Rate(10)
    # as long as you haven't ctrl + c keeping doing...
    while not rospy.is_shutdown():
        eval.update()
        r.sleep()
    
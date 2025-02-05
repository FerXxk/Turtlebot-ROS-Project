# Laboratorio de Robótica (4º GIERM)

In this repository, students will find the required files to complete the course on mobile robotics. The autonomous navigation folder consists on a simulation of the Turtlebot 3 in some maps, so we have designed a controller for the robot to move along a path while avoiding obstacles.

The challenge of reactive navigation has been completed succesfully following this steps:

1) At first, we subscribed the phython script to the topic movebase/goal to detect the objective that we wanted in Rviz. Next, we also subscribed to LaserScan to detect the surroundings of the robot. The first aproach to the movement controller was to calculate the distance and the angle from the robot to the objective. This was posible by transforming the global coordinates of the goal to the local reference of the Turtlebot. We made the robot move in proportion to this values, with an angular and linear velocity. Then we added some lines of code to avoid the columns of the map. 

2) The first thing we noticed was that when the robot detected an obstacle it entered in a loop, because the range that the LiDAR was looking was 360º. This made that when an obstacle was detected, it tried to rotate until the obstacle wasn't in the FOV. But instead of this the obstacle remained at the same distance, never stopping.

3) To fix this issue, we limited the range of the LiDAR to an angle of 90º looking to the front of the robot. After this change, the robot avoided the columns as it was required. The next step was to move along the path. 

4) We subscribed to the path that was published by path_publisher.py. Then we set the first coordinates of the path as the goal of the robot, and the same process as before was done, avoiding obstacles until reaching the goal. When the robot reaches it, the goal is updated with the next coordinates of the path. This happens until the path has no more points.

5) Then we tested our controller in the challenge_evaluation simulation. The larger walls proved the controller of the robot to be very inefficient. To improve the controller, we added a condition when detecting an obstacle. This condition consists in the robot looking to both sides of the obstacle when it is detected, surrounding it by the side that was closer to it. This change improved the navigation time and avoided all collisions. 

6) The final results are two different controllers for each simulation, both named robot_controller.py. The only major difference between them is the way that they obtain the points of the path as they are subscribed to different publishers and the points sent don´t have the same format. In this controllers the changes and improvements in the code are explained detailedly with their respective comments.

Authors: 
Fernando Román Hidalgo, José Chaqués Torres

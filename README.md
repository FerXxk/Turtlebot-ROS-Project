# Laboratorio de Robótica (4º GIERM)

In this repository, students will find the required files to complete the course on mobile robotics.

The challenge of reactive navigation has been completed succesfully following this steps:

1) At first, we subscribed the phython script to movebase/goal to detect the objective that we wanted in Rviz. Next, we also subscribed to LaserScan to detect the surroundings of the robot. Then we added some lines of code to avoid the columns of the map. 
The first thing we noticed was that when the robot detected an obstacle it entered in a loop, because the range of the LiDAR it was looking was 360º. This made that when an obstacle was detected, it tried to rotate until the obstacle wasn't there. But instead of this the obstacle remained at the same distance, so it never stopped.

2) To fix this issue, we limited the range of the LiDAR to an angle of 90º looking to the front of the robot. After this change, the robot avoided the columns as it was required. The next step was to move along the path. 

3) We subscribed to the path that was published by path_publisher.py. Then we set the first coordinates of the path as the goal of the robot, and the same process as before was done, avoiding obstacles until reaching the goal. When the robot reachs the goal, the goal is updated with the next coordinates of the path.

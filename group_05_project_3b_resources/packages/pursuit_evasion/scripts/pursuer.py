#!/usr/bin/env python
import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, PoseStamped
from move_base_msgs.msg import MoveBaseActionResult, MoveBaseGoal
from darknet_ros_msgs.msg import BoundingBoxes

initial_pose = PoseWithCovarianceStamped()
goal = PoseStamped()
pos_msg2= PoseStamped()

def update_initial_pose( initial_pose):
    x = initial_pose.pose.pose.position.x
    y = initial_pose.pose.pose.position.y
    z = initial_pose.pose.pose.position.z
    coord = ("Current coordinates of the turtlebot are :",x, y, z)
    rospy.loginfo(coord)

def callback(data):
	pub = rospy.Publisher('/tb3_0/move_base_simple/goal', PoseStamped, queue_size=100)	
	print(data.bounding_boxes)
	for box in data.bounding_boxes:
		midpoint_bbox = float((box.xmin + box.xmax)/2)
		print(midpoint_bbox)
		if box.probability>0.50:
			if 380 <= midpoint_bbox <= 420 and box.Class == "person":
				pos_msg2.header.frame_id = "map"
				pos_msg2.header.stamp=rospy.Time.now()
				pos_msg2.pose.orientation.z = 0
				pos_msg2.pose.position.x = 0
				pos_msg2.pose.position.y = 5
				pub.publish(pos_msg2)
			        print("Moving Forward")
			elif midpoint_bbox < 380 and box.Class == "person":
				pos_msg2.header.frame_id = "map"
				pos_msg2.header.stamp=rospy.Time.now()
				pos_msg2.pose.orientation.z = 0.5
				pos_msg2.pose.position.x = 0
				pos_msg2.pose.position.y = 0
				pub.publish(pos_msg2)
				print("Turning Left")

			elif midpoint_bbox > 420 and box.Class == "person":
				pos_msg2.header.frame_id = "map"
				pos_msg2.header.stamp=rospy.Time.now()
				pos_msg2.pose.orientation.z = -0.5
				pos_msg2.pose.position.x = 0
				pos_msg2.pose.position.y = 0
				pub.publish(pos_msg2)
				print("Turning Right")
		else:
			print("No person detected")
			pos_msg2.header.frame_id = "map"
			pos_msg2.header.stamp=rospy.Time.now()
			pos_msg2.pose.orientation.z = 0
			pos_msg2.pose.position.x = 0
			pos_msg2.pose.position.y = 0
			pub.publish(pos_msg2)

#def callback_(data):
#	print("scan")
#	print(data.ranges[180])

if __name__ == '__main__':
	rospy.init_node('listener', anonymous=True)
	sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, callback)
	rospy.Subscriber('/tb3_0/amcl_pose', PoseWithCovarianceStamped, update_initial_pose)
#	sub1 = rospy.Subscriber('tb3_0/scan', LaserScan, callback_)
	rospy.spin()

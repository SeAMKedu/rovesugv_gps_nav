import os
import sys

import rclpy
import yaml
from nav2_simple_commander.robot_navigator import BasicNavigator
from geographic_msgs.msg import GeoPose
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action._navigate_to_pose import NavigateToPose_Feedback
from robot_localization.srv import FromLL
from rclpy.node import Node

from rovesugv_gps_nav.gps_utils import latLonYaw2Geopose


class GPSWaypointCommander(Node):
    """GPS waypoint commander."""

    def __init__(self, yaml_filepath: str):
        super().__init__(node_name="gps_waypoint_commander")

        self.yaml_filepath = yaml_filepath

        self.client = self.create_client(srv_type=FromLL, srv_name="/fromLL")
        self.navigator = BasicNavigator()
        self.waypoints = []

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for 'FromLL' servive...")


    def follow_waypoints(self):
        """Start GPS waypoint following."""
        self.navigator.waitUntilNav2Active(localizer="controller_server")
        self.waypoints = self.get_waypoints()

        message = f"Following {len(self.waypoints)} waypoints"
        self.get_logger().info(message)

        poses = []
        for index, waypoint in enumerate(self.waypoints):
            self.request = FromLL.Request()
            self.request.ll_point.latitude = waypoint.position.latitude
            self.request.ll_point.longitude = waypoint.position.longitude
            self.request.ll_point.altitude = waypoint.position.altitude

            self.get_logger().info(f"Waypoint #{index + 1}")
            message = "lat={}, lon={}, alt={}".format(
                self.request.ll_point.latitude,
                self.request.ll_point.longitude,
                self.request.ll_point.altitude,
            )
            self.get_logger().info(message)

            self.future = self.client.call_async(self.request)
            rclpy.spin_until_future_complete(self, self.future)
            result: FromLL.Response = self.future.result()
            point = result.map_point

            self.goal_pose = PoseStamped()
            self.goal_pose.header.frame_id = "map"
            self.goal_pose.header.stamp = self.get_clock().now().to_msg()
            self.goal_pose.pose.position = point
            self.goal_pose.pose.orientation = waypoint.orientation

            message = f"x={point.x}, y={point.y}, z={point.z}"
            self.get_logger().info(message)

            poses += [self.goal_pose]

            self.navigator.goToPose(self.goal_pose)
            while not self.navigator.isTaskComplete():
                feedback: NavigateToPose_Feedback = self.navigator.getFeedback()
                if feedback:
                    print(feedback.distance_remaining)
            print(self.navigator.getResult())
        
        #self.navigator.followWaypoints(poses)


    def get_waypoints(self) -> list[GeoPose]:
        """Read GPS waypoints from the YAML file."""
        geoposes = []
        with open(self.yaml_filepath, "r") as yaml_file:
            filedata = yaml.safe_load(yaml_file)
            for wp in filedata["waypoints"]:
                lat, lon, yaw = wp["latitude"], wp["longitude"], wp["yaw"]
                geoposes.append(latLonYaw2Geopose(lat, lon, yaw))
        return geoposes


def main():
    rclpy.init()

    default_filepath = os.path.expanduser("~/gps_waypoints.yaml")
    filepath = sys.argv[1] if len(sys.argv) > 1 else default_filepath

    wp_commander = GPSWaypointCommander(filepath)
    wp_commander.follow_waypoints()

    rclpy.shutdown()


if __name__ == "__main__":
    main()

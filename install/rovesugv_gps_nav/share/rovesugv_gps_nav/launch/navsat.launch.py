import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    share_dir = get_package_share_directory("rovesugv_gps_nav")

    params_file = os.path.join(share_dir, "config", "navsat_params.yaml")

    # Robot localization is done by Fixposition device
    # --> use robot_localization package without EKFs.
    return LaunchDescription([
        Node(
            package="robot_localization",
            executable="navsat_transform_node",
            name="navsat_transform",
            output="screen",
            parameters=[params_file, {"use_sim_time": False}],
            remappings=[
                ("imu/data", "/fixposition/poiimu"),      # (Input) Message with orientation data
                ("odometry/filtered", "fixposition/odometry_enu"), # (Input) Robot"s current position
                ("gps/fix", "fixposition/odometry_llh"),  # (Input) Robot"s GPS coordinates
                ("odometry/gps", "odometry/gps"),         # (Output) Robot"s GPS coordinates, transformed into its world frame
                ("gps/filtered", "gps/filtered"),         # (Output) Robot’s world frame position, transformed into GPS coordinates
            ],
        ),
    ])

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # GPS navigation with the Fixposition GNSS receiver requires 
        # a transformation from 'vrtk_link' to robot's 'base_link'.
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="static_transform_vrtk_base",
            arguments=[
                "--x", "-0.185",
                "--y", "0.0",
                "--z", "-0.385",
                "--roll", "0.0",
                "--pitch", "0.0",
                "--yaw", "0.0",
                "--frame-id", "vrtk_link",
                "--child-frame-id", "panther/base_link"
            ]
        ),
    ])
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    nav2_dir = get_package_share_directory('nav2_bringup')

    # RViz2
    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_dir, 'launch', 'rviz_launch.py')
        ),
    )

    ld = LaunchDescription()
    ld.add_action(rviz_launch)

    return ld

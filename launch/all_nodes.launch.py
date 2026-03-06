# https://github.com/fixposition/nav2_tutorial/blob/main/README.md
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # Paths of the directories and files
    share_dir = get_package_share_directory('rovesugv_gps_nav')
    launch_dir = os.path.join(share_dir, 'launch')
    nav2_params = os.path.join(share_dir, 'config', 'nav2_params.yaml')

    # Fixposition to robot base link transformation
    fixpos_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'fixposition.launch.py')
        )
    )

    # Navigation2
    navigation2_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'navigation.launch.py')
        ),
        launch_arguments={
            'autostart': 'True',
            'namespace': 'panther',
            'params_file': nav2_params,
            'use_sim_time': 'False',
        }.items(),
    )

    # Start 'fromLL' service (among other services)
    navsat_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'navsat.launch.py')
        )
    )

    # Mapviz
    mapviz_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'mapviz.launch.py')
        )
    )

    # Create and populate launch description
    ld = LaunchDescription()

    ld.add_action(fixpos_cmd)
    ld.add_action(navsat_cmd)
    #ld.add_action(navigation2_cmd)
    #ld.add_action(mapviz_cmd)

    return ld
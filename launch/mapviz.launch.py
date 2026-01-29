import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

# Proxy server for Google Maps:
# https://github.com/danielsnider/MapViz-Tile-Map-Google-Maps-Satellite
# $ sudo docker run -p 8080:8080 -d -t -v ~/mapproxy:/mapproxy danielsnider/mapproxy

share_dir = get_package_share_directory('rovesugv_gps_nav')
mapviz_params = os.path.join(share_dir, "config", "mapviz.mvc")


def generate_launch_description():
    return LaunchDescription([
        # Spawn mapviz node
        Node(
            package="mapviz",
            executable="mapviz",
            name="mapviz",
            parameters=[{"config": mapviz_params}]
        ),
        # Spawn WGS84 to map transform
        Node(
            package="swri_transform_util",
            executable="initialize_origin.py",
            name="initialize_origin",
            remappings=[("fix", "fixposition/datum")],
        ),
        # Set up static transform between map and origin
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='swri_transform',
            output='screen',
            arguments=[
                '--x', '0',
                '--y', '0',
                '--z', '0',
                '--yaw', '0',
                '--pitch', '0',
                '--roll', '0',
                '--frame-id', 'map',
                '--child-frame-id', 'origin'
            ]
        )
    ])
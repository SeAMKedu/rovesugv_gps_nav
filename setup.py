import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'rovesugv_gps_nav'

setup(
    name=package_name,
    version='0.2.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Hannu Hakalahti',
    maintainer_email='hannu.hakalahti@seamk.fi',
    description='Development package for GPS navigation with Fixposition GNSS receiver',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'cmd_vel_converter = rovesugv_gps_nav.cmd_vel_converter:main',
            'gps_waypoint_logger = rovesugv_gps_nav.gps_waypoint_logger:main',
            'interactive_waypoint_follower = rovesugv_gps_nav.interactive_waypoint_follower:main',
            'logged_waypoint_follower = rovesugv_gps_nav.logged_waypoint_follower:main',
        ],
    },
)

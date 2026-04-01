import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/kayttaja/rovesugv/ros_ws/src/rovesugv_gps_nav/install/rovesugv_gps_nav'

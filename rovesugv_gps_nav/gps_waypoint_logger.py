import os
import json
import sys
from datetime import datetime

import customtkinter as ctk
import rclpy
import yaml
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

from rovesugv_gps_nav.gps_utils import euler_from_quaternion


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 310


class GPSWaypointLogger(ctk.CTk, Node):
    """
    GUI application for logging GPS waypoints to a file.

    """
    def __init__(self, yaml_filepath: str):
        ctk.CTk.__init__(self)
        Node.__init__(self, "gps_waypoint_logger")

        self.yaml_filepath = yaml_filepath

        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.grid_columnconfigure(0, weight=1)
        self.resizable(width=False, height=False)
        self.title("SEAMK | GPS Waypoint Logger")

        self.close = False
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Frame that shows the GPS coordinates and orientation.
        self.wp_frame = ctk.CTkFrame(self, width=360, height=150)
        self.wp_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.lat_label = ctk.CTkLabel(self.wp_frame, text="Latitude")
        self.lon_label = ctk.CTkLabel(self.wp_frame, text="Longitude")
        self.alt_label = ctk.CTkLabel(self.wp_frame, text="Altitude")
        self.yaw_label = ctk.CTkLabel(self.wp_frame, text="Yaw")

        self.lat_label.grid(row=0, column=0, padx=10)
        self.lon_label.grid(row=1, column=0, padx=10)
        self.alt_label.grid(row=2, column=0, padx=10)
        self.yaw_label.grid(row=3, column=0, padx=10)

        self.lat_value = ctk.CTkLabel(self.wp_frame, text="0.0")
        self.lon_value = ctk.CTkLabel(self.wp_frame, text="0.0")
        self.alt_value = ctk.CTkLabel(self.wp_frame, text="0.0")
        self.yaw_value = ctk.CTkLabel(self.wp_frame, text="0.0")

        self.lat_value.grid(row=0, column=1, padx=30)
        self.lon_value.grid(row=1, column=1, padx=30)
        self.alt_value.grid(row=2, column=1, padx=30)
        self.yaw_value.grid(row=3, column=1, padx=30)

        # Button for manually logging the GPS coordinates.
        self.btn1 = ctk.CTkButton(self, text="Log GPS Waypoint")
        self.btn1.configure(command=self.log_gps_waypoint)
        self.btn1.grid(row=1, column=0, padx=20, sticky="ew")

        # Frame that shows the controls for automatic GPS coordinate logging.
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.label1 = ctk.CTkLabel(self.log_frame, text="Automatic Waypoint Logging")
        self.label1.grid(row=0, column=0, padx=5, pady=5)

        self.label2 = ctk.CTkLabel(self.log_frame, text="OFF")
        self.label2.grid(row=0, column=1, padx=5)

        self.btn2 = ctk.CTkButton(
            self.log_frame, 
            text="Enable",
            fg_color="#009933",
            hover_color="#006600",
            command=self.on_auto_log_enable, 
        )
        self.btn2.grid(row=1, column=0, padx=5, pady=5)

        self.btn3 = ctk.CTkButton(
            self.log_frame, 
            text="Disable",
            fg_color="#ff0000",
            hover_color="#cc0000",
            command=self.on_auto_log_disable,
        )
        self.btn3.grid(row=1, column=1, padx=5, pady=5)

        self.label3 = ctk.CTkLabel(self.log_frame, text="Logging Interval (s)")
        self.label3.grid(row=2, column=0, padx=5)

        self.option_menu = ctk.CTkOptionMenu(
            self.log_frame, 
            values=["1", "3", "5", "10"],
            command=self.on_option_menu_value_change,
        )
        self.option_menu.grid(row=2, column=1, padx=5)

        # ROS 2 definitions
        self.navsatfix_msg = NavSatFix()
        self.navsatfix_sub = self.create_subscription(
            msg_type=NavSatFix,
            topic="/fixposition/odometry_llh",
            callback=self.navsatfix_callback,
            qos_profile=10,
        )

        self.yaw = 0.0
        self.odometry_sub = self.create_subscription(
            msg_type=Odometry,
            topic="/fixposition/odometry_enu",
            callback=self.odometry_callback,
            qos_profile=10,
        )

        self.timer = self.create_timer(1.0, self.log_gps_waypoint)
        self.timer.cancel()
       

    def on_auto_log_enable(self):
        """Enable the automatic GPS waypoint logging."""
        self.timer.reset()
        self.label2.configure(text="ON")


    def on_auto_log_disable(self):
        """Disable the automatic GPS waypoint logging."""
        self.timer.cancel()
        self.label2.configure(text="OFF")


    def on_close(self):
        """Called when the window is closed."""
        self.close = True


    def on_option_menu_value_change(self, choice: str):
        """Change the timer period."""
        self.timer.timer_period_ns = int(choice) * 1_000_000_000


    def odometry_callback(self, msg: Odometry):
        """Called when an Odometry message is published."""
        _, _, self.yaw = euler_from_quaternion(msg.pose.pose.orientation)
        self.yaw_value.configure(text=f"{self.yaw:.12f}")


    def navsatfix_callback(self, msg: NavSatFix):
        """Called when a NavSatFix message is published."""
        self.navsatfix_msg = msg
        self.lat_value.configure(text=f"{msg.latitude:.12f}")
        self.lon_value.configure(text=f"{msg.longitude:.12f}")
        self.alt_value.configure(text=f"{msg.altitude:.12f}")


    def log_gps_waypoint(self):
        """Write a GPS waypoint to YAML file."""
        try:
            with open(self.yaml_filepath, "r") as yaml_file:
                filedata = yaml.safe_load(yaml_file)
        except FileNotFoundError:
            message = f"YAML file '{self.yaml_filepath}' not found"
            self.get_logger().error(message)
            sys.exit(1)

        waypoint = {
            "latitude": self.navsatfix_msg.latitude,
            "longitude": self.navsatfix_msg.longitude,
            #"altitude": self.navsatfix_msg.altitude,
            "yaw": self.yaw,
            #"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        #self.get_logger().info(json.dumps(waypoint))

        if not filedata: # empty file
            filedata = {"waypoints": []}
        try:
            filedata["waypoints"].append(waypoint)
        except AttributeError:
            filedata = {"waypoints": []}
            filedata["waypoints"].append(waypoint)

        with open(self.yaml_filepath, "w") as yaml_file:
            yaml.dump(filedata, yaml_file)


def main():
    rclpy.init()

    default_filepath = os.path.expanduser("~/gps_waypoints.yaml")
    filepath = sys.argv[1] if len(sys.argv) > 1 else default_filepath

    app = GPSWaypointLogger(filepath)

    while rclpy.ok():
        rclpy.spin_once(app, timeout_sec=0.1)
        app.update()
        if app.close:
            app.destroy()
            break
    
    rclpy.try_shutdown()


if __name__ == "__main__":
    main()

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class CmdVelSubPub(Node):
    """
    Subscribe to the navigation command velocity topic and publish its
    messages to the Panther's command velocity topic.

    """

    def __init__(self):
        super().__init__(node_name='cmd_vel_sub_pub')
        self.subscription = self.create_subscription(
            msg_type=Twist,
            topic='cmd_vel_nav',
            callback=self.listener_callback,
            qos_profile=10,
        )
        self.publisher = self.create_publisher(
            msg_type=Twist,
            topic='panther/cmd_vel',
            qos_profile=10,
        ) 
    
    def listener_callback(self, msg: Twist):
        self.publisher.publish(msg)


def main():
    rclpy.init()
    node = CmdVelSubPub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

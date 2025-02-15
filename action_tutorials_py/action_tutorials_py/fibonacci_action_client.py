#!/usr/bin/python3

from action_tutorials_interfaces.action import Fibonacci
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        # Wait for action server to be available
        self.get_logger().info('Waiting for action server...')
        if not self._action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Action server not available after waiting')
            return

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info(f'Sending goal request with order: {order}')

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)
        
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            rclpy.shutdown()
            return

        self.get_logger().info('Goal accepted')
        
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Final sequence: {result.sequence}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.partial_sequence}')


def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    
    try:
        # Get input from user
        while True:
            try:
                order = int(input('Enter Fibonacci sequence length (positive integer): '))
                if order <= 0:
                    print('Please enter a positive integer')
                    continue
                break
            except ValueError:
                print('Please enter a valid integer')
    
        action_client.send_goal(order)
        rclpy.spin(action_client)
    
    except KeyboardInterrupt:
        print('\nClient stopped by user')
    finally:
        # Ensure proper shutdown
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
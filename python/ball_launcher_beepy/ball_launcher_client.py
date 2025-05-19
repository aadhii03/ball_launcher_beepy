import logging

import zmq

from .ball_launcher_pb2 import Request


class BallLauncherClient:
    """Client sending commands to the ball launcher.

    Uses ZeroMQ for communication with server.
    """

    def __init__(self, ip_address: str, port_number: int) -> None:
        """Set up ball launcher client.

        Expects ip address of server as string and port number.
        """

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        logging.info(f"tcp://{ip_address}:{port_number}")
        self.socket.connect(f"tcp://{ip_address}:{port_number}")

    def set_state(
        self,
        phi: float,
        theta: float,
        top_left_motor: float = 0.0,
        top_right_motor: float = 0.0,
        bottom_motor: float = 0.0,
    ) -> None:
        """Set orientation of launcher and motor speeds.

        Arguments:
        phi -- azimuthal angle of launcher (in [0, 1])
        theta -- altitude of launcher (in [0, 1])
        top_left_motor -- activation of top left motor (in [0, 1], default 0.0)
        top_left_motor -- activation of top right motor (in [0, 1], default 0.0)
        bottom_motor -- activation of bottom motor (in [0, 1], default 0.0)
        """

        # communicate request to server using protobuf
        request = Request()

        request.request = Request.RequestType.Value("SET_STATE")
        request.state.phi = phi
        request.state.theta = theta
        request.state.top_left_motor = top_left_motor
        request.state.top_right_motor = top_right_motor
        request.state.bottom_motor = bottom_motor

        self.socket.send(request.SerializeToString())

        # Get the reply
        message = self.socket.recv()
        print(message)
        if message == "0":
            raise Exception("Ball launcher server failed to process SET_STATE request.")

    def set_rpm(
        self,
        phi: float,
        theta: float,
        top_left_motor: float = 0.0,
        top_right_motor: float = 0.0,
        bottom_motor: float = 0.0,
    ) -> None:
        """Set orientation of launcher and motor speeds.

        Arguments:
        phi -- azimuthal angle of launcher (in [0, 1])
        theta -- altitude of launcher (in [0, 1])
        top_left_motor -- activation of top left motor (in [0, 1], default 0.0)
        top_left_motor -- activation of top right motor (in [0, 1], default 0.0)
        bottom_motor -- activation of bottom motor (in [0, 1], default 0.0)
        """

        # communicate request to server using protobuf
        request = Request()

        request.request = Request.RequestType.Value("SET_RPM")
        request.state.phi = phi
        request.state.theta = theta
        request.state.top_left_motor = top_left_motor
        request.state.top_right_motor = top_right_motor
        request.state.bottom_motor = bottom_motor

        self.socket.send(request.SerializeToString())

        # Get the reply
        message = self.socket.recv()
        if message == "0":
            raise Exception("Ball launcher server failed to process SET_STATE request.")


    def launch_ball(self) -> None:
        """Launches ball."""
        # communicate request to server using protobuf
        request = Request()
        request.request = Request.RequestType.Value("LAUNCH_BALL")

        self.socket.send(request.SerializeToString())

        # Get the reply
        message = self.socket.recv()
        if message == "0":
            raise Exception(
                "Ball launcher server failed to process LAUNCH_BALL request."
            )

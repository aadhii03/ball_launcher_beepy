import zmq

from .ball_launcher_control import BallLauncherControl
from .ball_launcher_pb2 import Request


class BallLauncherServer:
    """Server waiting for commands for the ball launcher.

    Uses ZeroMQ for communication with clients. Uses BallLauncher
    object for control of ball launcher."""

    def __init__(self, port_number: int):
        """Set up ball launcher server. Expects port number."""

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{port_number}")

        # BallLauncher object that controls servos. Initialized at neutral orientation,
        # wheels at rest.
        self.launcher = BallLauncherControl()

    def run(self):
        """Run server which starts to listen to messages from clients containing
        requests for the ball launcher."""

        while True:
            try:

                # Wait for next request from client, NOBLOCK will raise EAGAIN if
                # the event cannot be completed.
                message = self.socket.recv(flags=zmq.NOBLOCK)
                print("Connection established")

                request = Request()
                # Process message using protobuf
                request.ParseFromString(message)

                # Use ball launcher to realize request
                if request.request == Request.RequestType.SET_STATE:
                    self.launcher.set_state(
                        phi=request.state.phi,
                        theta=request.state.theta,
                        top_left_motor=request.state.top_left_motor,
                        top_right_motor=request.state.top_right_motor,
                        bottom_motor=request.state.bottom_motor,
                    )
                elif request.request == Request.RequestType.SET_RPM:
                    self.launcher.set_rpm(
                        request.state.phi,
                        request.state.theta,
                        request.state.top_left_motor,
                        request.state.top_right_motor,
                        request.state.bottom_motor,
                    )
                elif request.request == Request.RequestType.LAUNCH_BALL:
                    self.launcher.launch_ball()
                else:
                    raise Exception(
                        f"Ball launcher server: Unknown request type: {request.request}"
                    )
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    # called when socket does not receive a message
                    #self.launcher.check_ball_supply()
                    pass
            except Exception:
                # returns
                self.socket.send(b"0")
            else:
                self.socket.send(b"1")

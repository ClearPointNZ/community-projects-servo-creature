import time
from inputs import get_gamepad
import threading


class XboxController(object):
    def __init__(self):

        self.LeftDPad = False
        self.RightDPad = False
        self.UpDPad = False
        self.DownDPad = False

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):  # return the buttons/triggers that you care about in this method
        return [self.LeftDPad, self.RightDPad, self.UpDPad, self.DownDPad]

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_HAT0Y':
                    self.UpDPad = event.state == -1
                    self.DownDPad = event.state == 1
                elif event.code == 'ABS_HAT0X':
                    self.LeftDPad = event.state == -1
                    self.RightDPad = event.state == 1


if __name__ == '__main__':
    joy = XboxController()
    try:
        while True:
            time.sleep(0.5)
            [left, right, up, down] = joy.read()
            print("Left: {0}, Right: {1}, Up: {2}, Down: {3}".format(left, right, up, down))
    except KeyboardInterrupt:
        exit(1)

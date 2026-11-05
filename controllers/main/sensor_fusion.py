import numpy as np


class SensorFusion:
    """
    Combines the e-puck distance sensors with camera/YOLO information.

    The e-puck has 8 distance sensors:
        ds0, ds7 -> front
        ds1, ds6 -> front-left / front-right
        ds2, ds5 -> left / right
        ds3, ds4 -> rear
    """

    def __init__(self, robot, sensor_max=1000.0):
        self.robot = robot
        self.sensor_max = sensor_max

    def get_sensor_data(self):
        values = self.robot.get_distances()

        # Group sensors according to their orientation.
        front = float(np.max(values[[0, 7]]))
        front_left = float(values[1])
        front_right = float(values[6])
        left = float(values[2])
        right = float(values[5])
        rear_left = float(values[3])
        rear_right = float(values[4])

        return {
            "front": front,
            "front_left": front_left,
            "front_right": front_right,
            "left": left,
            "right": right,
            "rear_left": rear_left,
            "rear_right": rear_right,
            "raw": values,
        }

    def get_risk(self, value):
        """
        Convert sensor strength into a simple risk level.

        NOTE:
        Webots sensor values are raw values, so we will calibrate
        these thresholds after observing the real values.
        """
        if value >= 800:
            return "HIGH"
        elif value >= 400:
            return "MEDIUM"
        else:
            return "LOW"

    def analyze(self):
        data = self.get_sensor_data()

        return {
            "data": data,
            "front_risk": self.get_risk(data["front"]),
            "left_risk": self.get_risk(data["left"]),
            "right_risk": self.get_risk(data["right"]),
        }

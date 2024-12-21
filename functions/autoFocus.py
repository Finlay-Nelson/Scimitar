
"""

A first attempt at enabling autofocus with the motorised objective

"""

import numpy as np
import cv2  # For focus metric calculation

from pipython import GCSDevice
from uc480 import Camera

def calculate_focus_metric(image):
    """
    Calculate focus quality using the variance of the Laplacian.
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()

def initialize_stage():
    controller = GCSDevice('E-873')  # Controller name
    controller.ConnectUSB()  # Establish connection via USB
    axes = controller.qSAI()  # Query axes
    print(f"Connected to controller. Axes available: {axes}")
    return controller

def move_stage_to_position(controller, axis, position):
    controller.MOV(axis, position)  # Move stage to position
    controller.WAIT(axis)  # Wait for the move to complete
    print(f"Moved to position {position}")

def capture_image():
    with Camera() as cam:
        cam.open()
        cam.start_live_video()  # Live video mode
        frame = cam.capture_frame()  # Capture an image
        cam.stop_live_video()
        return frame


def autofocus(controller, axis, start_pos, end_pos, step_size, camera):
    """
    Perform autofocus by scanning the Z-axis.
    """
    best_focus = -1
    best_position = None

    for pos in np.arange(start_pos, end_pos, step_size):
        # Move the stage
        controller.MOV(axis, pos)
        controller.WAIT(axis)

        # Capture an image
        image = camera.capture_frame()
        focus_metric = calculate_focus_metric(image)

        # Find the best focus
        if focus_metric > best_focus:
            best_focus = focus_metric
            best_position = pos

    # Move to the best focus position
    controller.MOV(axis, best_position)
    controller.WAIT(axis)
    print(f"Autofocus complete. Best position: {best_position}, Focus metric: {best_focus}")

# Main script
if __name__ == "__main__":
    # Initialize hardware
    controller = GCSDevice('E-873')
    controller.ConnectUSB()
    axis = "Z"

    with Camera() as camera:
        # Perform autofocus
        autofocus(controller, axis, start_pos=0.0, end_pos=10.0, step_size=0.1, camera=camera)

    controller.CloseConnection()

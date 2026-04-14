"""Camera pose conversions — quaternion ↔ euler ↔ spherical."""

import numpy as np
from spark_viewer.backend import CameraPose


def quaternion_to_euler(wxyz: tuple) -> tuple:
    """Convert quaternion (w,x,y,z) to euler angles (roll, pitch, yaw) in degrees."""
    w, x, y, z = wxyz

    # Roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.degrees(np.arctan2(sinr_cosp, cosr_cosp))

    # Pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = np.degrees(np.copysign(np.pi / 2, sinp))
    else:
        pitch = np.degrees(np.arcsin(sinp))

    # Yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.degrees(np.arctan2(siny_cosp, cosy_cosp))

    return roll, pitch, yaw


def viser_to_camera_pose(wxyz: tuple, position: tuple) -> CameraPose:
    """Convert Viser camera state to our CameraPose.
    
    Viser gives us:
    - wxyz: quaternion orientation (w, x, y, z)
    - position: camera world position (x, y, z)
    
    We convert to spherical:
    - yaw: left/right angle in degrees
    - pitch: up/down angle in degrees  
    - zoom: distance from origin
    """
    roll, pitch, yaw = quaternion_to_euler(wxyz)
    
    # Distance from origin = zoom
    pos = np.array(position)
    zoom = float(np.linalg.norm(pos))
    if zoom < 1e-6:
        zoom = 1.0

    return CameraPose(
        yaw=yaw,
        pitch=pitch,
        zoom=zoom,
        wxyz=wxyz,
        position=position,
    )


def poses_differ(a: CameraPose, b: CameraPose, 
                 angle_threshold: float = 0.5,
                 zoom_threshold: float = 0.01) -> bool:
    """Check if two poses are meaningfully different."""
    if a is None or b is None:
        return True
    return (
        abs(a.yaw - b.yaw) > angle_threshold
        or abs(a.pitch - b.pitch) > angle_threshold
        or abs(a.zoom - b.zoom) > zoom_threshold
    )

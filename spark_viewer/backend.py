"""Backend interface — what each AI project implements."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import numpy as np


@dataclass
class CameraPose:
    """Universal camera pose representation."""
    yaw: float = 0.0          # degrees, left/right
    pitch: float = 0.0        # degrees, up/down
    zoom: float = 1.0         # distance multiplier
    # Raw Viser data preserved for backends that want it
    wxyz: Optional[tuple] = None       # quaternion (w, x, y, z)
    position: Optional[tuple] = None   # (x, y, z) world coords


@dataclass
class RenderSettings:
    """What the user has configured via GUI."""
    width: int = 832
    height: int = 480
    denoising_steps: list = field(default_factory=lambda: [1000, 750, 500, 250])
    guidance_scale: float = 3.0
    use_tae: bool = True
    compile_dit: bool = True


@dataclass
class RenderResult:
    """What the backend returns after neural refinement."""
    image: np.ndarray              # HxWx3 uint8
    elapsed_seconds: float = 0.0
    metadata: Optional[dict] = None


class Backend(ABC):
    """Interface that each AI project implements.
    
    To create a new backend:
    1. Subclass Backend
    2. Implement the 4 required methods
    3. Pass an instance to SparkViewer
    """

    @abstractmethod
    def load_scene(self, input_path: str, progress_callback=None) -> dict:
        """Preprocess input (video/image/etc) → return scene data.
        
        Must return a dict. The viewer will pass this dict back to
        get_point_cloud() and render().
        
        Called once per input. Can be slow (preprocessing).
        progress_callback("message") to update status in GUI.
        """
        pass

    @abstractmethod
    def get_point_cloud(self, scene_data: dict) -> tuple:
        """Return (points, colors) for the 3D viewer.
        
        points: numpy array shape (N, 3) float32
        colors: numpy array shape (N, 3) uint8 (0-255)
        """
        pass

    @abstractmethod
    def render(self, scene_data: dict, pose: CameraPose,
               settings: RenderSettings) -> RenderResult:
        """Run neural refinement at the given camera pose.
        
        Called when camera stops moving (or manually triggered).
        Return a RenderResult with the refined image.
        """
        pass

    @abstractmethod
    def get_presets(self) -> dict:
        """Return available quality presets for the GUI.
        
        Format: {
            "Preset Name": {
                "width": 416,
                "height": 240,
                "denoising_steps": [1000, 250],
                ...any RenderSettings fields...
            }
        }
        """
        pass

    def cleanup(self):
        """Optional cleanup when viewer shuts down."""
        pass

    def supports_streaming(self) -> bool:
        """If True, render() may be called continuously for live frames.
        If False (default), only called after camera stops."""
        return False

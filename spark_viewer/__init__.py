"""spark-viewer — Modular real-time 3D viewer for AI/neural rendering."""

from spark_viewer.viewer import SparkViewer
from spark_viewer.backend import Backend, CameraPose, RenderSettings, RenderResult

__version__ = "0.1.0"
__all__ = ["SparkViewer", "Backend", "CameraPose", "RenderSettings", "RenderResult"]

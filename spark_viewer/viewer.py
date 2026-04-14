"""SparkViewer — Main viewer class that wires everything together."""
# Stub — full implementation next session

import time


class SparkViewer:
    """Reusable interactive 3D viewer with neural refinement."""

    def __init__(self, backend, port=7861, title="Spark Viewer"):
        self.backend = backend
        self.port = port
        self.title = title
        # Full implementation will initialize:
        # - viser.ViserServer
        # - SceneManager
        # - GUIBuilder
        # - GPUMemoryManager
        # - RefinementLoop

    def load(self, input_path: str):
        """Load an input (video/image) → preprocess → show point cloud."""
        pass

    def run(self):
        """Start the viewer (blocks)."""
        pass

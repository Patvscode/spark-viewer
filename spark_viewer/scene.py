"""SceneManager — load and manage 3D scene objects."""
# Stub — full implementation next session


class SceneManager:
    """Manages point clouds and 3D objects in the Viser scene."""

    def __init__(self, server):
        self.server = server
        self._point_cloud = None

    def set_point_cloud(self, points, colors, point_size=0.02):
        """Load a point cloud into the scene."""
        pass

    def clear(self):
        """Remove all scene objects."""
        pass

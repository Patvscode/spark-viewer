"""RefinementLoop — camera tracking + debounce + backend trigger."""
# Stub — full implementation next session


class RefinementLoop:
    """Watches camera pose, triggers backend render when camera stops."""

    def __init__(self, server, backend, gui, gpu_mgr):
        self.server = server
        self.backend = backend
        self.gui = gui
        self.gpu_mgr = gpu_mgr
        self.scene_data = None

    def set_scene(self, scene_data):
        """Set the active scene for refinement."""
        self.scene_data = scene_data

    def start(self):
        """Start the camera tracking loop in a background thread."""
        pass

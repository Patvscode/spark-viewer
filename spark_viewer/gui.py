"""GUIBuilder — standard controls factory."""
# Stub — full implementation next session


class GUIBuilder:
    """Standard GUI controls that any backend can use."""

    def __init__(self, server, presets):
        self.server = server
        self.presets = presets

    def get_render_settings(self):
        """Return current RenderSettings from GUI state."""
        pass

    def set_status(self, text):
        """Update status display."""
        pass

    def update_progress(self, msg):
        """Update progress during scene loading."""
        pass

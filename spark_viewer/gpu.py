"""GPUMemoryManager — stop/start llama-servers for inference."""
# Stub — will be copied from inspatio-world/app.py and generalized next session


class GPUMemoryManager:
    """Manages GPU memory by stopping/starting model servers."""

    def stop_servers(self):
        """Free GPU memory by stopping llama-servers."""
        pass

    def restart_servers(self):
        """Restore llama-servers after inference."""
        pass

    def get_status(self) -> str:
        """Return current GPU status string."""
        return "unknown"

# spark-viewer

Modular real-time 3D viewer framework for AI/neural rendering apps on DGX Spark.

Built on [Viser](https://github.com/viser-project/viser) — provides a reusable interactive viewer with point cloud rendering, camera controls, GUI panels, and a plugin backend interface for neural refinement.

## What it does

- **Real-time 3D navigation** — orbit, zoom, pan at 60fps in your browser
- **Neural refinement overlay** — when you stop moving, an AI model refines the view
- **Pluggable backends** — swap out the AI model without touching the viewer
- **Built-in GUI** — quality sliders, auto-refine toggle, status bar
- **GPU management** — automatically frees GPU for inference, restores after
- **Works anywhere** — browser-based, accessible over Tailscale/SSH

## Architecture

```
spark-viewer (reusable)          Backend (per-project)
┌─────────────────────┐          ┌─────────────────┐
│ SceneManager        │          │ load_scene()     │
│ GUIBuilder          │◄────────►│ get_point_cloud()│
│ RefinementLoop      │          │ render()         │
│ GPUMemoryManager    │          │ get_presets()    │
│ PoseConverter       │          └─────────────────┘
└─────────────────────┘
        │
   Viser (Three.js)
        │
    Browser @ :7861
```

## Quick Start

```python
from spark_viewer import SparkViewer
from my_project.backend import MyBackend

viewer = SparkViewer(MyBackend(), port=7861, title="My App")
viewer.load("input_video.mp4")
viewer.run()
```

## Writing a Backend

Implement 4 methods:

```python
from spark_viewer.backend import Backend, CameraPose, RenderSettings, RenderResult

class MyBackend(Backend):
    def load_scene(self, input_path, progress_callback=None) -> dict:
        """Preprocess input → return scene data dict."""
        ...
    
    def get_point_cloud(self, scene_data) -> tuple:
        """Return (points_Nx3, colors_Nx3_uint8)."""
        ...
    
    def render(self, scene_data, pose, settings) -> RenderResult:
        """Neural refinement at given camera pose."""
        ...
    
    def get_presets(self) -> dict:
        """Resolution/quality presets for GUI."""
        ...
```

## Backends

| Backend | Project | Status |
|---------|---------|--------|
| InSpatioBackend | [InSpatio-World](https://github.com/inspatio/inspatio-world) | 🔧 Building |
| WorldFMBackend | [WorldFM](https://github.com/inspatio/worldfm) | 📋 Planned |
| OverworldBackend | [World Engine](https://github.com/Overworldai/world_engine) | 📋 Planned |
| StaticBackend | Generic PLY viewer | 📋 Planned |

## Requirements

- Python 3.10+
- DGX Spark (or any NVIDIA GPU for backends)
- `pip install viser plyfile numpy`

## License

MIT

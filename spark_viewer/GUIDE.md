# spark-viewer (3D Interactive Viewer) — Guide

## What This Does
Gives you a real-time 3D point cloud viewer in the browser with built-in camera controls (orbit, zoom, pan), GUI panels (sliders, buttons), and a "neural refinement" loop that can call an AI model to enhance what you're looking at. Think of it like Google Earth but for AI-generated 3D scenes.

## When To Use This
- You have a 3D point cloud (PLY file) and want to view/explore it interactively
- You have an AI model that can render/refine views of a 3D scene
- You want a browser-based UI with camera controls and settings panels
- You need to let a user explore a scene and trigger AI rendering at specific viewpoints

## When NOT To Use This
- You just need to show a static image — use Gradio or a simple web page
- You need video playback, not interactive 3D — use a video player
- Your model generates 2D images with no 3D component — this is overkill
- You need <10ms latency real-time rendering — the DiT/neural path is too slow

## Prerequisites

### System
- DGX Spark (or any machine with Python 3.10+)
- A browser (Chrome, Firefox, Safari — works on phone too)
- Network access between server and browser (localhost, or Tailscale for remote)

### Python Packages
```bash
pip install viser plyfile numpy
```

### What is Viser?
Viser is a Python library that creates a 3D viewer in your browser. You write Python code, it shows 3D stuff in a web page. It handles all the Three.js/WebGL/WebSocket stuff internally. You never write JavaScript.

### What is a PLY file?
A PLY (Polygon File Format) file stores 3D point clouds — lists of (x, y, z) coordinates with colors. They're produced by 3D scanning, depth estimation, photogrammetry, etc. Ours come from the DA3 depth estimation model.

## Setup (Step by Step)

### Step 1: Install the package
```bash
cd ~/Desktop/AI-apps-workspace/spark-viewer
pip install -e .
```
**Expected output:** `Successfully installed spark-viewer-0.1.0`  
**If it fails:** Make sure you have Python 3.10+. Check with `python3 --version`.

### Step 2: Verify viser works
```bash
python3 -c "import viser; s = viser.ViserServer(port=7899); print('Viser OK'); s.close()"
```
**Expected output:** `Viser OK` (may also print a URL)  
**If it fails with ImportError:** Run `pip install viser` again.  
**If it fails with "port in use":** Change 7899 to another port, or kill whatever's using it: `lsof -ti:7899 | xargs kill`

### Step 3: Verify PLY loading works
```bash
python3 -c "
from plyfile import PlyData
import numpy as np
# Create a tiny test point cloud
print('plyfile OK')
"
```
**Expected output:** `plyfile OK`

## Usage Examples

### Example 1: Minimal Point Cloud Viewer (no AI, just viewing)

This is the simplest possible use. Load a PLY file, view it in the browser.

```python
#!/usr/bin/env python3
"""Minimal point cloud viewer — no AI backend."""
import time
import numpy as np
import viser
from plyfile import PlyData

# Start server
server = viser.ViserServer(port=7861)

# Load point cloud from PLY
ply = PlyData.read("/path/to/your/point_cloud.ply")
v = ply['vertex']
points = np.stack([v['x'], v['y'], v['z']], axis=-1).astype(np.float32)

# Colors: PLY stores as 0-255 uint8
colors = np.stack([v['red'], v['green'], v['blue']], axis=-1).astype(np.uint8)

# Add to scene
server.scene.add_point_cloud(
    "/world",
    points=points,
    colors=colors,
    point_size=0.02,  # Adjust this — bigger = more visible but chunkier
)

# Add a slider to control point size
point_size_slider = server.gui.add_slider(
    "Point Size", min=0.005, max=0.1, step=0.005, initial_value=0.02
)

@point_size_slider.on_update
def _(_):
    server.scene.add_point_cloud(
        "/world", points=points, colors=colors, 
        point_size=point_size_slider.value
    )

print(f"Viewer running at http://localhost:7861")
print(f"Or via Tailscale: http://100.109.173.109:7861")

# Keep running
while True:
    time.sleep(1.0)
```

**To run:** `python3 minimal_viewer.py`  
**Then open:** `http://localhost:7861` in your browser  
**Controls:** Left-click drag = orbit, scroll = zoom, right-click drag = pan

### Example 2: With Camera Tracking (see where user is looking)

```python
#!/usr/bin/env python3
"""Track camera pose — prints where the user is looking."""
import time
import viser

server = viser.ViserServer(port=7861)

# Add something to look at
import numpy as np
points = np.random.randn(10000, 3).astype(np.float32)
colors = np.random.randint(0, 255, (10000, 3), dtype=np.uint8)
server.scene.add_point_cloud("/test", points=points, colors=colors, point_size=0.03)

status = server.gui.add_text("Camera", initial_value="Move the camera...", disabled=True)

while True:
    clients = server.get_clients()
    for client_id, client in clients.items():
        wxyz = client.camera.wxyz       # Quaternion (w, x, y, z)
        pos = client.camera.position    # World position (x, y, z)
        fov = client.camera.fov         # Field of view in degrees
        status.value = f"Pos: ({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}) | FOV: {fov:.0f}°"
    time.sleep(0.2)
```

### Example 3: With AI Backend (the full pattern)

```python
#!/usr/bin/env python3
"""Full pattern — viewer + AI refinement backend."""
from spark_viewer import SparkViewer
from spark_viewer.backend import Backend, CameraPose, RenderSettings, RenderResult
import numpy as np

class MyBackend(Backend):
    def load_scene(self, input_path, progress_callback=None):
        if progress_callback:
            progress_callback("Loading scene...")
        # Your preprocessing here
        return {"path": input_path}
    
    def get_point_cloud(self, scene_data):
        # Return your point cloud data
        from plyfile import PlyData
        ply = PlyData.read(scene_data["path"])
        v = ply['vertex']
        points = np.stack([v['x'], v['y'], v['z']], axis=-1).astype(np.float32)
        colors = np.stack([v['red'], v['green'], v['blue']], axis=-1).astype(np.uint8)
        return points, colors
    
    def render(self, scene_data, pose, settings):
        # Your AI model inference here
        # Return a refined image as numpy array (H, W, 3) uint8
        fake_image = np.zeros((settings.height, settings.width, 3), dtype=np.uint8)
        return RenderResult(image=fake_image, elapsed_seconds=0.1)
    
    def get_presets(self):
        return {
            "Fast": {"width": 416, "height": 240},
            "Quality": {"width": 832, "height": 480},
        }

viewer = SparkViewer(MyBackend(), port=7861)
viewer.load("path/to/point_cloud.ply")
viewer.run()
```

## Common Problems & Solutions

| Problem | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: No module named 'viser'` | viser not installed | `pip install viser` |
| `OSError: [Errno 98] Address already in use` | Port 7861 already taken | Kill it: `lsof -ti:7861 \| xargs kill` or use a different port |
| Browser shows blank page | Wrong URL or server not started | Check terminal for the URL. Make sure you see "Viser running" |
| Point cloud looks too small/big | Point size or camera distance off | Adjust `point_size` parameter. Try 0.01-0.05. Zoom with scroll wheel |
| Can't access from phone | Server bound to localhost | Viser binds 0.0.0.0 by default. Access via Tailscale IP: `http://100.109.173.109:7861` |
| PLY file won't load | Wrong format or missing color data | Check with: `python3 -c "from plyfile import PlyData; p=PlyData.read('file.ply'); print(p['vertex'].data.dtype.names)"` — should show x,y,z,red,green,blue |
| Colors look wrong (all gray/black) | Colors stored as float 0-1 instead of uint8 0-255 | Multiply by 255 and cast: `colors = (colors * 255).astype(np.uint8)` |
| `CUDA out of memory` during DiT render | GPU full from other models | Use GPUMemoryManager to stop llama-servers first |
| Viewer is laggy with huge point clouds | Too many points (>5M) | Subsample: `indices = np.random.choice(len(points), 500000, replace=False)` |

## Configuration Options

| Setting | Type | Default | What it does | When to change it |
|---------|------|---------|-------------|-------------------|
| `port` | int | 7861 | HTTP/WebSocket port for the viewer | If 7861 is taken |
| `point_size` | float | 0.02 | Size of each point in the cloud | If points look too sparse (increase) or too blobby (decrease) |
| `auto_refine` | bool | True | Auto-trigger DiT when camera stops | Turn off if you just want to browse without GPU usage |
| `refine_delay` | float | 1.5 | Seconds to wait after camera stops before triggering DiT | Lower = more responsive but more GPU. Higher = only refines deliberate pauses |
| `quality_preset` | str | middle | Which resolution/steps preset to use | Depends on whether you want speed or quality |

## How It Works (Internal)

### Architecture
```
SparkViewer (orchestrator)
├── ViserServer (from pip viser) — handles browser, WebSocket, Three.js
├── SceneManager — loads PLY data into Viser scenes
├── GUIBuilder — creates sliders/buttons via Viser's gui API
├── RefinementLoop (background thread)
│   ├── Polls client.camera every 100ms
│   ├── Detects when camera stops (pose unchanged for refine_delay seconds)
│   ├── Calls Backend.render() with current pose
│   └── Overlays result via server.scene.set_background_image()
├── GPUMemoryManager — stops/starts llama-servers to free VRAM
└── Backend (your AI code) — implements 4 methods
```

### Camera Pose Flow
1. User drags mouse → Viser updates `client.camera.wxyz` (quaternion) and `client.camera.position` (xyz)
2. RefinementLoop converts quaternion → spherical angles (yaw, pitch) + distance (zoom) via `pose.py`
3. Backend receives `CameraPose(yaw, pitch, zoom)` and renders from that angle
4. Result image is set as background via `server.scene.set_background_image()`

### Why Quaternions?
Viser (and Three.js internally) represents camera orientation as a quaternion (w, x, y, z) — four numbers that describe rotation without gimbal lock. Our `pose.py` converts these to the simpler yaw/pitch/zoom that most backends expect. You don't need to understand quaternions to use this — the conversion is automatic.

## Limitations

- **Not real-time neural rendering.** The point cloud layer is 60fps, but DiT refinement takes seconds. This is a "preview + refine" workflow, not a game engine.
- **Single user.** Camera tracking follows one client. Multi-user would need per-client refinement queues.
- **No mesh rendering.** This shows point clouds, not solid surfaces. Points have gaps between them.
- **GPU contention.** DiT inference stops other GPU models (llama-servers). The GPUMemoryManager handles this but there's a brief interruption.
- **Browser memory.** Very large point clouds (>10M points) may slow down the browser. Subsample if needed.

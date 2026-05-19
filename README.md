<div align="center">

# Omniverse Kit — Live Webcam

**A custom NVIDIA Kit editor extension that streams your system webcam into a USD scene in real time**

[![Kit App Template](https://img.shields.io/badge/NVIDIA-Kit%20App%20Template-76b900?logo=nvidia&logoColor=white)](https://github.com/NVIDIA-Omniverse/kit-app-template)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![USD](https://img.shields.io/badge/USD-OpenUSD-76b900?logo=nvidia&logoColor=white)](https://openusd.org/)

*Live webcam feed · `omni.ui` viewport window · OmniPBR USD texture · Kit editor integration*

[Overview](#overview) · [How It Works](#how-it-works) · [Project Structure](#project-structure) · [Installation](#installation) · [Build & Launch](#build--launch) · [Extension Details](#extension-details)

</div>

---

## Overview

**`omni.webcam.viewport`** (*Webcam to Stage*) is a Python extension for the [NVIDIA Kit App Template](https://github.com/NVIDIA-Omniverse/kit-app-template) that bridges your system webcam and a live USD scene. Once launched inside the custom Kit editor, the extension:

- Captures the system webcam stream using **OpenCV**
- Displays the feed in a floating **`omni.ui`** window inside the Kit editor
- Textures a USD mesh (`/World/CCTV_Screen`) in the main Omniverse viewport using **OmniPBR** and **UsdUVTexture** — so the live feed appears on a physical surface in 3D

The sample application (`source/apps/my_company.my_editor.kit`) declares `"omni.webcam.viewport"` as a dependency, so the extension loads automatically when the editor starts.

---

## How It Works

```
System Webcam
      │
      │  cv2.VideoCapture
      ▼
┌─────────────────────┐
│   OpenCV Frame Loop  │   Reads frames at runtime in a background thread
└──────────┬──────────┘
           │  raw BGR frame
           ▼
┌─────────────────────┐
│   omni.ui Window    │   Displays the live feed inside the Kit editor UI
└──────────┬──────────┘
           │  frame bytes → dynamic texture
           ▼
┌──────────────────────────┐
│   USD Texture Update     │   Writes pixels to UsdUVTexture asset bound
│   /World/CCTV_Screen     │   to OmniPBR material on the stage mesh
└──────────────────────────┘
           │
           ▼
   Main Omniverse Viewport
   (live webcam on a 3D surface)
```

### Key components

| Component | Role |
|---|---|
| **OpenCV (`cv2`)** | Webcam capture and frame decoding |
| **`omni.ui`** | Floating editor window displaying the raw stream |
| **`UsdUVTexture`** | USD texture prim updated each frame with webcam pixels |
| **OmniPBR material** | PBR shader bound to `/World/CCTV_Screen` mesh |
| **Kit App Template** | Build system, repo tooling, and extension loader |

---

## Project Structure

```text
omniverse-kit-webcam/
│
├── source/
│   ├── apps/
│   │   └── my_company.my_editor.kit      # Kit app config — declares omni.webcam.viewport
│   │
│   └── extensions/
│       └── omni.webcam.viewport/
│           ├── omni/webcam/viewport/
│           │   ├── extension.py          # Extension entry point (startup / shutdown)
│           │   ├── webcam_window.py      # omni.ui window with live feed
│           │   └── texture_writer.py     # UsdUVTexture update loop
│           ├── config/
│           │   └── extension.toml        # Extension metadata and dependencies
│           └── data/                     # Static assets (USD stage, materials)
│
├── environment.yml                       # Conda environment (omni-webcam)
├── repo.bat                              # Windows build / launch script
├── repo.sh                               # Linux build / launch script
└── README.md
```

---

## Installation

### Prerequisites

- **NVIDIA Omniverse** installed ([download](https://www.nvidia.com/en-us/omniverse/))
- **Conda** (Miniconda or Anaconda)
- A connected webcam (USB or built-in)
- Windows 10/11 or Ubuntu 20.04+

### 1. Clone the repository

```bash
git clone https://github.com/kamranghz/omniverse-kit-webcam.git
cd omniverse-kit-webcam
```

### 2. Create the Conda environment

```bash
conda env create -f environment.yml
conda activate omni-webcam
```

---

## Build & Launch

All commands are run from the repository root with the `omni-webcam` environment active.

### Windows

```powershell
.\repo.bat build
.\repo.bat launch
```

### Linux

```bash
./repo.sh build
./repo.sh launch
```

The Kit editor opens with the **Webcam to Stage** panel loaded automatically. The webcam stream starts as soon as the extension initialises.

---

## Extension Details

### Extension identifier

```
omni.webcam.viewport
```

### App configuration

The sample `.kit` file at `source/apps/my_company.my_editor.kit` declares the extension as a dependency:

```toml
[dependencies]
"omni.webcam.viewport" = {}
```

This ensures the extension is resolved and loaded every time the editor launches — no manual activation required.

### USD stage setup

The extension expects a mesh prim at `/World/CCTV_Screen` in the active stage, bound to an OmniPBR material with a `UsdUVTexture` node. The texture node's pixel data is overwritten each frame with the latest webcam capture, creating the live-feed effect on the 3D surface.

To use a different mesh path, update the prim target in `texture_writer.py`.

---

## Upstream Resources

This workspace is built on the official NVIDIA Kit App Template. For full documentation on the build system, extension authoring, and deployment:

- [Kit App Template — Getting Started](https://docs.omniverse.nvidia.com/kit/docs/kit-app-template/latest/docs/intro.html)
- [NVIDIA-Omniverse/kit-app-template](https://github.com/NVIDIA-Omniverse/kit-app-template)
- [Omniverse Extensions documentation](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/extensions_intro.html)


---

## Author

**Kamran Gholizadeh HamlAbadi**
PhD Candidate, University of Ottawa · MCRLab
[github.com/kamranghz](https://github.com/kamranghz) · [LinkedIn](https://www.linkedin.com/in/kamrangh)

# Omniverse Kit — Live Webcam 

**Repository:** [github.com/kamranghz/omniverse-kit-webcam](https://github.com/kamranghz/omniverse-kit-webcam)

This directory is the **NVIDIA [Kit App Template](https://github.com/NVIDIA-Omniverse/kit-app-template)**–style workspace used to build a custom Kit editor. The project adds a Python extension, **`omni.webcam.viewport`** (*Webcam to Stage*), which uses **OpenCV** to read the system webcam, shows the stream in a Kit **`omni.ui`** window, and textures a USD mesh (**`/World/CCTV_Screen`**) in the main viewport via **OmniPBR** and **UsdUVTexture**.

The sample application **`source/apps/my_company.my_editor.kit`** declares **`"omni.webcam.viewport"`** so the extension loads with the editor.

---

## Build and launch

From **this folder**, with Conda env **`omni-webcam`** created from **`environment.yml`**:

```bash
# Windows
.\repo.bat build
.\repo.bat launch

# Linux
./repo.sh build
./repo.sh launch
```

---

## Docs in this tree

| File | Contents |
|------|----------|
| [README_WEBCAM_EXTENSION.md](README_WEBCAM_EXTENSION.md) | Extension setup, USD paths, troubleshooting |
| [source/extensions/omni.webcam.viewport/README.md](source/extensions/omni.webcam.viewport/README.md) | Extension package and main source files |

---

## Upstream Kit template

Templates, repo tooling, and NVIDIA’s full guide: **[Kit App Template tutorial](https://docs.omniverse.nvidia.com/kit/docs/kit-app-template/latest/docs/intro.html)** · **[NVIDIA-Omniverse/kit-app-template](https://github.com/NVIDIA-Omniverse/kit-app-template)**

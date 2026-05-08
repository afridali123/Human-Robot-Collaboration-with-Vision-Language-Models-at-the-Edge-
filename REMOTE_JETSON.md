# Remote Jetson Workflow

Use this when the Jetson AGX Orin is reachable over SSH.

## 1. Copy Repo to Jetson

From your laptop:

```bash
rsync -av --exclude .venv --exclude __pycache__ ./ <JETSON_USER>@<JETSON_IP>:~/vlm-jetson-demo/
```

Or clone the repo directly on the Jetson when it is hosted in Git.

## 2. Run One-Time Setup

SSH into the Jetson:

```bash
ssh <JETSON_USER>@<JETSON_IP>
cd ~/vlm-jetson-demo
cp .env.example .env
nano .env
./scripts/setup_jetson.sh
```

Log out and back in if Docker group membership was changed.

## 3. Validate

```bash
cd ~/vlm-jetson-demo
./scripts/doctor.sh
```

## 4. Open VS Code Remotely

Install the VS Code Remote SSH extension, connect to `<JETSON_USER>@<JETSON_IP>`, and open:

```text
~/vlm-jetson-demo
```

Use the tasks in `.vscode/tasks.json` for setup checks, camera capture, VLM image demo, and RTSP/JPS helpers.

## 5. Common Commands

```bash
./scripts/demo_camera_capture.sh --no-preview
./scripts/demo_image_vlm.sh images/capture.jpg "What should the robot do?"
./scripts/start_rtsp_server.sh
./scripts/register_rtsp_with_jps.sh
./scripts/demo_jps_ask.sh "What do you see?"
```

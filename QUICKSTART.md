# Quickstart

Run these commands on the Jetson AGX Orin after copying or cloning this repo.

```bash
cd ~/vlm-jetson-demo
cp .env.example .env
./scripts/setup_jetson.sh
./scripts/doctor.sh
```

Capture a frame:

```bash
./scripts/demo_camera_capture.sh
```

Ask the image VLM:

```bash
./scripts/demo_image_vlm.sh images/capture.jpg "What objects can the robot interact with?"
```

Start the Jetson-native container:

```bash
./scripts/run_container.sh
```

For the JPS RTSP path:

```bash
./scripts/start_rtsp_server.sh
./scripts/stream_usb_to_rtsp.sh /dev/video0 rtsp://127.0.0.1:8554/camera
python3 scripts/jps_vlm_demo.py add-stream --api http://127.0.0.1:5010 --rtsp rtsp://127.0.0.1:8554/camera
```

Then set `JPS_STREAM_ID` in `.env` and run:

```bash
./scripts/demo_jps_ask.sh "What do you see?"
```

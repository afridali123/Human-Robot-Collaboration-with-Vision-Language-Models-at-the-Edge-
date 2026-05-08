.PHONY: setup-local doctor camera image-vlm rtsp-up rtsp-down jps-register jps-ask

setup-local:
	./scripts/setup_local.sh

doctor:
	./scripts/doctor.sh

camera:
	./scripts/demo_camera_capture.sh

image-vlm:
	./scripts/demo_image_vlm.sh

rtsp-up:
	./scripts/start_rtsp_server.sh

rtsp-down:
	./scripts/stop_rtsp_server.sh

jps-register:
	./scripts/register_rtsp_with_jps.sh

jps-ask:
	./scripts/demo_jps_ask.sh

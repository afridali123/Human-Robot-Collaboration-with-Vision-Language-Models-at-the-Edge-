# Human-Robot-Collaboration-with-Vision-Language-Models-at-the-Edge
# 🚀 Vision-Language Models on Jetson AGX Orin  
### Edge AI for Human-Robot Collaboration  

Deploy Vision-Language Models (VLMs) on **NVIDIA Jetson AGX Orin** to enable robots and edge devices to **see, understand, and reason** in real time.

---

## 🎯 Project Overview

This project demonstrates how to build an **end-to-end edge AI pipeline**:

📷 Camera Input → 🧠 Vision-Language Model → 💬 Natural Language Understanding → 🤖 Action/Decision  

It showcases how **computer vision + GenAI** can enable **human-robot collaboration at the edge**.

---

## 🧠 Key Features

- Run **Vision-Language Models (VLMs)** like LLaVA / BLIP on Jetson  
- Real-time **image understanding and Q&A**  
- Camera-based **live inference pipeline**  
- Lightweight **agent logic for decision-making**  
- Designed for **robotics, IoT, and edge AI applications**  

---

## 🏗️ System Architecture

```text
Camera / Image Input
        ↓
Object Detection (YOLO - TensorRT)
        ↓
Scene Understanding
        ↓
Vision-Language Model (LLaVA / BLIP)
        ↓
Prompt + Query
        ↓
GenAI Agent Logic
        ↓
Robot / IoT Action
```

## 🛠️ Tech Stack
Hardware: NVIDIA Jetson AGX Orin
Frameworks: PyTorch, Hugging Face Transformers
Acceleration: TensorRT (optional optimization)
Vision Models: YOLOv8
VLM Models: LLaVA / BLIP
Tools: OpenCV, Docker, jetson-containers

## 📁 Project Structure
```text
vlm-jetson-demo/
├── README.md
├── app/
│   ├── vlm_image_demo.py
│   ├── camera_capture.py
│   ├── agent_logic.py
├── images/
│   └── sample.jpg
├── scripts/
│   ├── run_container.sh
│   └── check_camera.sh
└── requirements.txt
```

## ⚙️ Setup Instructions
1. Clone Repository
git clone https://github.com/your-username/vlm-jetson-demo.git
cd vlm-jetson-demo
2. Prepare Jetson Environment
sudo apt update
sudo apt install -y python3-pip python3-venv git

(Optional: enable max performance)

sudo nvpmodel -m 0
sudo jetson_clocks
3. Install Dependencies
pip3 install torch torchvision transformers opencv-python pillow
4. (Recommended) Use Jetson Containers
git clone https://github.com/dusty-nv/jetson-containers
cd jetson-containers
bash install.sh

## Run container:

jetson-containers run $(autotag llava)
▶️ Running the Demo
📷 Step 1: Capture Image
python3 app/camera_capture.py --camera 0 --output images/capture.jpg
🧠 Step 2: Run VLM
python3 app/vlm_image_demo.py \
  --image images/capture.jpg \
  --prompt "Describe the objects in this scene."
🤖 Step 3: Agent Decision
python3 app/agent_logic.py
💡 Example Output
Input: "What do you see?"

Output:
"There is a red box and a bottle on a table."

## Action:
→ Robot can pick the red box
🚀 Use Cases
🤖 Human-Robot Collaboration
📦 Smart Warehousing
🏙️ Smart Surveillance
🏥 Healthcare Assistants
🌱 Edge AI for IoT Systems
⚡ Optimization Tips
Use FP16 / INT8 quantization
Convert models → ONNX → TensorRT
Reduce image resolution for faster inference
Use smaller VLM models for edge deployment

##🧪 Future Improvements
Add real-time video streaming pipeline
Integrate ROS2 for robot control
Add voice input (Whisper) + speech output (TTS)
Deploy via Flask / FastAPI API service
Optimize using TensorRT-LLM / Edge AI SDKs

## 👤 Author

Afrid Thenebanda
Speaker @ India Electronics Week 2026
Focus: Robotics | Computer Vision | Edge AI
##⭐ Support

If you found this useful, please ⭐ star the repo!

---

# 🚀 Pro Tip (Important for You)

After publishing:
- Add this repo to your **LinkedIn post**
- Mention:
  👉 *“Live demo code for my India Electronics Week talk”*

This instantly boosts your **visibility + credibility**.

---

If you want next:
- I can help you **create requirements.txt**
- Or build a **clean demo UI (Gradio/Web app)**
- Or make your repo look like a **top-tier GitHub project (badges, banners, visuals)**

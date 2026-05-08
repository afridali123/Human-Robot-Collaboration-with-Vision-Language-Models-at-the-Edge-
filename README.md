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

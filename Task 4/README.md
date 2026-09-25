# Radar Speed Detector

## Overview
A vehicle speed detection system using YOLO object detection and ByteTrack tracking.

The system detects vehicles, tracks each vehicle with a unique ID, and calculates its speed between two virtual lines.

## Technologies
- Python
- YOLOv8
- ByteTrack
- OpenCV

## Features
- Vehicle detection
- Vehicle tracking using ByteTrack
- Vehicle IDs
- Speed calculation in km/h
- Real-time display of detected vehicles and speed

## Speed Calculation
The real-world distance between the two virtual lines is 9.144 meters.

Speed is calculated using:

Speed = Distance / Time × 3.6

The time is calculated from the video frame numbers and the video's FPS.

## Project Structure
- `speed_detector.py` — main speed detection and tracking program
- `Train_Model.py` — YOLO model training
- `training.ipynb` — training notebook and evaluation results
- `requirements.txt` — required Python libraries

## Dataset
The project uses a vehicle detection dataset containing YOLO-formatted annotations.

## Tracking
ByteTrack is used to maintain vehicle identities across video frames.

## Notes
The trained model and dataset are not included directly in the repository.

# Guard-X AI Surveillance System

<div align="center">
  <img src="https://img.shields.io/badge/AI-Powered-brightgreen" alt="AI Powered">
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Status">
  <img src="https://img.shields.io/badge/Version-2.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</div>

## Overview

Guard-X is an advanced AI-powered surveillance system designed for military and security applications. It combines cutting-edge computer vision, drone fleet management, and real-time threat detection to provide comprehensive surveillance solutions for high-risk environments.

### Key Features

- **AI-Powered Detection**: Advanced YOLO-based neural networks for real-time human activity detection
- **Drone Fleet Management**: Centralized control and monitoring of multiple surveillance drones
- **Real-Time Analytics**: Live threat assessment with confidence scoring
- **Tactical Mapping**: Interactive map interface with drone positioning and coverage areas
- **Military-Grade Security**: JWT-based authentication with role-based access control
- **Edge Computing**: Optimized for deployment in remote and challenging environments

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Engine     │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (PyTorch)     │
│                 │    │                 │    │                 │
│ • Drone Fleet   │    │ • REST APIs     │    │ • YOLO Models   │
│ • Live Map      │    │ • WebSockets    │    │ • Detection     │
│ • Analytics     │    │ • Auth System   │    │ • Classification│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Technology Stack

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Lucide React** - Professional icons

### Backend
- **FastAPI** - High-performance Python web framework
- **Uvicorn** - ASGI server for production
- **PyTorch** - Deep learning framework
- **OpenCV** - Computer vision library
- **Ultralytics YOLO** - Object detection models

### AI/ML
- **YOLOv8** - Real-time object detection
- **Custom CNN Models** - Specialized threat detection
- **Edge Computing** - Optimized inference
- **Thermal Imaging Support** - Multi-spectrum analysis

## Installation

### Prerequisites
- Python 3.11+ (Recommended)
- Node.js 18+
- Git

### Backend Setup

```bash
# Clone repository
git clone https://github.com/your-org/guard-x-surveillance.git
cd guard-x-surveillance/Backend

# Create virtual environment
python -m venv myenv
myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Start server
python run_server.py
```

### Frontend Setup

```bash
# Navigate to frontend
cd ../Frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Usage

### 1. Authentication
```bash
# Default credentials
Username: admin
Password: guard-x-2024
```

### 2. Drone Fleet Management
- Monitor live drone positions on tactical map
- Deploy drones to specific patrol areas
- Track battery levels and operational status
- Receive real-time threat alerts

### 3. AI Detection
- Upload images/video for analysis
- Real-time human activity detection
- Confidence scoring and threat assessment
- Historical detection logs

### 4. API Integration
```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/health")

# Upload for detection
files = {"file": open("image.jpg", "rb")}
response = requests.post("http://localhost:8000/api/detect", files=files)
```

## Project Structure

```
guard-x-surveillance/
├── Backend/
│   ├── app.py                 # Main FastAPI application
│   ├── model_wrapper.py       # AI model interface
│   ├── auth.py               # Authentication system
│   ├── camera_detection.py   # Real-time detection
│   ├── models/               # AI model files
│   └── requirements.txt      # Python dependencies
├── Frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── DroneFleet.jsx
│   │   │   ├── DroneMap.jsx
│   │   │   ├── Detection.jsx
│   │   │   └── About.jsx
│   │   ├── App.jsx          # Main application
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Build configuration
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User authentication
- `GET /api/auth/me` - Get current user info

### Detection
- `POST /api/detect` - Single image detection
- `GET /api/detections/swarm` - Drone fleet detections
- `GET /api/health` - System health check

### Drone Management
- `GET /api/drones` - List all drones
- `POST /api/drones/deploy` - Deploy drone to area
- `GET /api/drones/{id}/status` - Get drone status

## Configuration

### Environment Variables
```bash
# Backend/.env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MODEL_PATH=models/best.pt
```

### Model Configuration
Place your trained YOLO model at `Backend/models/best.pt` or the system will use the default YOLO model.

## Development

### Adding New Features
1. Backend: Add endpoints in `app.py`
2. Frontend: Create components in `src/components/`
3. AI Models: Update `model_wrapper.py`

### Testing
```bash
# Backend tests
cd Backend
python -m pytest

# Frontend tests
cd Frontend
npm test
```

## Deployment

### Production Setup
```bash
# Backend
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
# Serve dist/ folder with nginx/apache
```

## Team

- **Ayush Kumar** 
- **Ashish Kumar** 
- **Ayoan Singh** 
- **Aryan Kumar** 
- **Ayushman Praharaj** 

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Security Notice

This is a military-grade surveillance system. Ensure proper security measures are in place before deployment in production environments.


https://github.com/user-attachments/assets/f21886b6-1e80-4104-bd7b-9439fb9f35b0



<img width="1897" height="861" alt="Screenshot 2025-09-20 044648" src="https://github.com/user-attachments/assets/6083a83f-c71c-4f40-8602-420fe650c3dd" />
<img width="1895" height="867" alt="Screenshot 2025-09-20 044631" src="https://github.com/user-attachments/assets/b61b2825-03c7-4f37-8cd0-b02802ee9d88" />
<img width="1896" height="864" alt="Screenshot 2025-09-20 044607" src="https://github.com/user-attachments/assets/b0d99595-ae64-4c86-b8e3-7816a7c0ec7c" />
<img width="1896" height="865" alt="Screenshot 2025-09-20 044552" src="https://github.com/user-attachments/assets/590cdf2f-d358-4478-9695-9c6f8f6e3c91" />
<img width="1898" height="863" alt="Screenshot 2025-09-20 044537" src="https://github.com/user-attachments/assets/acee9c46-53f8-4222-8eec-decc00c58f09" />
<img width="1891" height="866" alt="Screenshot 2025-09-20 044521" src="https://github.com/user-attachments/assets/0e84ab28-768a-4912-82b0-bd312a85a35c" />
<div align="center">
  <strong>Guard-X AI Surveillance System</strong><br>
  Advanced AI-Powered Security Solutions
</div>







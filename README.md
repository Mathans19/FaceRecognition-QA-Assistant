# Face Recognition AI with RAG-Powered Q&A System

A comprehensive face recognition system with an intelligent Q&A assistant powered by Retrieval-Augmented Generation (RAG) technology.

## 🌟 Features

- **Real-time Face Recognition**: Live video feed processing with OpenCV
- **Face Registration**: Easy enrollment system for new users
- **Intelligent Q&A**: RAG-powered chatbot that answers questions about registration and recognition data
- **Modern Web Interface**: Beautiful React-based chat interface with WebSocket real-time communication

The system consists of:
1. **Frontend**: React.js chat interface with WebSocket communication
2. **WebSocket Server**: Node.js server handling real-time messaging
3. **RAG Engine**: FastAPI backend with LangChain and Google Gemini
4. **Face Recognition**: Python-based registration and recognition modules
5. **Database**: SQLite for storing face encodings and activity logs

## 🔧 Prerequisites

- Python 3.8+
- Node.js 16+
- OpenCV-compatible camera
- Google API Key for Gemini LLM

## 📋 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Mathans19/FaceRecognition-QA-Assistant.git
```

### 2. Backend Setup (Python)
```bash
# Create virtual environment
python -m venv venv
On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 4. Node.js Server Setup
```bash
# Install Node.js dependencies
cd rag-node-backend
npm install
```

### 5. Frontend Setup
```bash
# Install React dependencies
cd rag-react-frontend
npm install
```

## 🚀 Running the Application

### Start the Services in Order:

1. **Start the RAG Engine (FastAPI)**:
```bash
python -m uvicorn main:app --reload --port 8000
```

2. **Start the WebSocket Server**:
```bash
cd rag-node-backend
node server.js
```

3. **Start the Frontend**:
```bash
cd frontend
cd rag-react-frontend
npm start
```

4. **Register Faces** (in a separate terminal):
```bash
python register.py
```

5. **Start Live Recognition** (in another terminal):
```bash
python live_feed.py
```

## 📊 Usage

### Face Registration
1. Run `python register.py`
2. Enter your name when prompted
3. Press 's' to capture your face when ready
4. Your face encoding will be stored in the database

### Live Recognition
1. Run `python live_feed.py`
2. The system will recognize registered faces in real-time
3. Recognition events are logged to the database

### Q&A Chat Interface
1. Open your browser to `http://localhost:3000`
2. Ask questions about registration and recognition activities
3. Examples:
   - "Who was registered today?"
   - "Show me all recognition logs"
   - "When was John last seen?"
   - "How many people are registered?"

## 🗂️ Project Structure

```
face-recognition-rag-system/
├── main.py                 # FastAPI RAG engine
├── register.py             # Face registration module
├── live_feed.py           # Real-time recognition module
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── face_recognition.db    # SQLite database (created on first run)
├── rag-react-frontend/     # React frontend
│   ├── src/
│   │   ├── app.js
│   │   ├── chatwidget.js
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   └── package.json
├── rag-node-backend/          #Node Backend
│   ├── server.js              # Node.js WebSocket server
│   ├── package.json           # Node.js dependencies
└── architecture.svg
```

## 📝 Database Schema

### Registrations Table
```sql
CREATE TABLE registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL,
    registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Recognition Logs Table
```sql
CREATE TABLE recognition_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    recognized_at TEXT NOT NULL
);
``


## 🤔 Assumptions Made

Based on the requirements, the following assumptions were made:

1. **Hardware**: Users have access to a camera-enabled device for face recognition
2. **Environment**: Development environment with Python 3.8+ and Node.js 16+
3. **API Access**: Users can obtain and configure Google Gemini API key
4. **Network**: Local development environment with standard ports (3000, 3001, 8000) available
5. **Data Privacy**: Face encodings are stored locally in SQLite database
6. **Usage Pattern**: Primary use case is for small to medium-scale face recognition (< 1000 faces)
7. **Recognition Accuracy**: Acceptable false positive/negative rates for demonstration purposes
8. **Concurrent Users**: System designed for single-user demonstration, not high-concurrency production use

## 🛠️ Technical Stack

- **Frontend**: React.js, WebSocket, Modern CSS with Glassmorphism
- **Backend**: FastAPI, LangChain, HuggingFace Embeddings
- **AI/ML**: Google Gemini LLM, FAISS Vector Store, Face Recognition Library
- **Database**: SQLite
- **Communication**: WebSocket for real-time messaging
- **Computer Vision**: OpenCV, face_recognition library

## 🔒 Security Considerations

- Face encodings are stored as binary data, not raw images
- Local database storage (not cloud-based)
- API keys stored in environment variables
- No personal image data transmitted over network


**This project is a part of a hackathon run by https://katomaran.com**

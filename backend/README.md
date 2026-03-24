# LevelUp FastAPI Backend

Python FastAPI backend for the LevelUp gamified life system.

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

### 4. Run the Server

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload --port 5000
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## 🔧 Development

### Project Structure

```
backend/
├── app/
│   ├── config/          # Settings and database
│   ├── models/          # Pydantic models
│   ├── routes/          # API endpoints
│   ├── services/        # AI service
│   ├── utils/           # XP calculator
│   └── main.py          # FastAPI app
├── tests/               # Tests
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
└── run.py              # Startup script
```

### Key Features

- ✅ Async MongoDB with Motor
- ✅ Anthropic Claude AI integration
- ✅ Auto-generated API docs
- ✅ Type safety with Pydantic
- ✅ CORS enabled for frontend

## 🧪 Testing

```bash
pytest
```

## 📦 Deployment

### Railway.app (Recommended)

1. Connect your GitHub repo
2. Set environment variables
3. Deploy automatically

### Docker

```bash
docker build -t levelup-backend .
docker run -p 5000:5000 levelup-backend
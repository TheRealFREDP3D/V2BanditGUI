# Bandit-NG 🎯

> **AI-powered terminal interface for OverTheWire Bandit CTF challenges**

A split-screen web application that combines the classic Bandit CTF experience with an AI mentor (Neo from The Matrix) to guide you through cybersecurity concepts without spoilers.

![Bandit-NG Interface](https://img.shields.io/badge/Status-Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Modern web browser
- 2GB+ RAM (for Ollama model)

### One-Command Setup

```bash
git clone <repository-url>
cd V2BanditGUI
docker-compose up --build
```

Open [http://localhost:8000](http://localhost:8000) in your browser and start hacking!

## 🎮 Features

### 🤖 AI Mentor (Neo)

- **Character-driven guidance**: Neo explains concepts like a 90s hacker
- **Spoiler-free approach**: Never gives direct commands, only explains concepts
- **Context-aware**: Analyzes your terminal history and current level
- **Local-first**: Uses Ollama for privacy and zero cost

### 🖥️ Terminal Interface

- **Real-time SSH**: Direct connection to OverTheWire Bandit servers
- **WebSocket-powered**: Responsive terminal experience
- **Auto-reconnection**: Handles connection drops gracefully
- **Keyboard shortcuts**: Ctrl+M for quick mentor access

### 🔒 Security & Ethics

- **Rate limiting**: Prevents API abuse (1 request per 90 seconds)
- **Command filtering**: Guards against direct command suggestions
- **No credential storage**: Passwords never logged or stored
- **Local AI**: Your data stays on your machine

## 🏗️ Architecture

```
┌─────────────────┐    WebSocket    ┌─────────────────┐
│   Browser       │ ◄─────────────► │   FastAPI       │
│   (xterm.js)    │                 │   (Python)      │
└─────────────────┘                 └─────────────────┘
                                              │
                                              │ SSH
                                              ▼
                                    ┌─────────────────┐
                                    │   OverTheWire   │
                                    │   Bandit        │
                                    └─────────────────┘
                                              │
                                              │ LLM
                                              ▼
                                    ┌─────────────────┐
                                    │   Ollama        │
                                    │   (Local AI)    │
                                    └─────────────────┘
```

## 📁 Project Structure

```
V2BanditGUI/
├── app/
│   ├── main.py          # FastAPI server + WebSocket + SSH bridge
│   ├── mentor.py        # AI mentor logic & prompt engineering
│   └── config.py        # Configuration management
├── static/
│   ├── js/
│   │   ├── terminal.js  # xterm.js + WebSocket client
│   │   └── mentor.js    # Mentor UI & API calls
│   ├── index.html       # Main application interface
│   └── styles.css       # Matrix-style theming
├── docs/
│   └── _DEV_/          # Development documentation
├── docker-compose.yml   # Multi-container orchestration
├── Dockerfile          # Python application container
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Optional: Google Gemini API key for cloud AI
GEMINI_API_KEY=your_gemini_api_key_here

# Ollama host (default: http://localhost:11434)
OLLAMA_HOST=http://ollama:11434

# Rate limiting (default: 1 request per 90 seconds)
RATE_LIMIT=1/90second
```

### AI Models

- **Default**: `qwen2.5:1.5b` (local via Ollama)
- **Cloud**: Google Gemini (if API key provided)
- **Custom**: Add your own models via Ollama

## 🧠 How It Works

### 1. **Connection Flow**

1. Browser connects to FastAPI via WebSocket
2. FastAPI establishes SSH connection to Bandit server
3. Real-time bidirectional data flow begins

### 2. **Mentor System**

1. User types commands in terminal
2. System captures last 20 lines + current level
3. Context sent to AI with Neo personality prompt
4. Response filtered for commands, returned as guidance

### 3. **Security Measures**

- Regex filtering removes direct command suggestions
- Rate limiting prevents abuse
- Input validation on all endpoints
- Error handling with user-friendly messages

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama separately
docker run -d -p 11434:11434 ollama/ollama

# Run FastAPI with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run tests
pytest

# E2E tests with Playwright
playwright test
```

### Building

```bash
# Build Docker image
docker build -t bandit-ng .

# Run standalone
docker run -p 8000:8000 bandit-ng
```

## 🐛 Troubleshooting

### Common Issues

**"Connection failed"**

- Check if OverTheWire servers are accessible
- Verify network connectivity
- Try refreshing the page

**"Rate limit exceeded"**

- Wait 90 seconds between mentor requests
- This is intentional to prevent abuse

**"Model not found"**

- First mentor request downloads the model (~2 minutes)
- Check Ollama container logs: `docker logs <ollama-container>`

**Terminal not responding**

- Check WebSocket connection in browser dev tools
- Verify SSH connection in FastAPI logs
- Try reconnecting by refreshing the page

### Logs

```bash
# View application logs
docker-compose logs app

# View Ollama logs
docker-compose logs ollama

# Follow logs in real-time
docker-compose logs -f
```

## 🤝 Contributing

### Development Guidelines

1. **Keep it simple**: Resist feature creep
2. **Test thoroughly**: Add tests for new features
3. **Document changes**: Update docs for API changes
4. **Follow style**: Use existing code patterns

### Code Style

- Python: Black formatting, type hints
- JavaScript: ES2023 modules, no build step
- CSS: Custom properties, mobile-first

### Testing

- Unit tests: `pytest`
- Integration tests: `pytest-asyncio`
- E2E tests: `playwright`

## 📚 Learning Resources

### Bandit CTF

- [OverTheWire Bandit](https://overthewire.org/wargames/bandit/)
- [Bandit Level Solutions](https://overthewire.org/wargames/bandit/bandit0.html)

### Technologies Used

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [xterm.js Documentation](https://xtermjs.org/)
- [Ollama Documentation](https://ollama.ai/)
- [Paramiko SSH](https://www.paramiko.org/)

## 📄 License

This project is open source. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **OverTheWire**: For the amazing Bandit CTF challenges
- **Ollama**: For local AI inference
- **FastAPI**: For the excellent web framework
- **xterm.js**: For the terminal emulator

---

**Remember**: The goal is to learn, not just solve. Let Neo guide you through the concepts! 🕶️

*"Unfortunately, no one can be told what the Matrix is. You have to see it for yourself."*

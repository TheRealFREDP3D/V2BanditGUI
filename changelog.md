# Changelog

All notable changes to the Bandit-NG project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Project documentation and overview
- Requirements.txt for dependency management
- Environment configuration template (.env.example)
- This CHANGELOG.md file

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [0.1.0] - 2025-01-XX (Initial Implementation)

### Added
- FastAPI backend with WebSocket support for terminal sessions
- SSH connection to OverTheWire Bandit servers using paramiko
- AI mentor system using Ollama/Qwen2.5:1.5b with Neo persona
- XTerm.js-based web terminal interface
- Rate limiting (1 request per 90 seconds) to prevent abuse
- Command redaction system to prevent cheating
- Matrix-themed dark UI design
- Split-screen layout with terminal and mentor panels
- Keyboard shortcut support (Ctrl+M for mentor)
- Environment-based configuration management
- Static file serving for frontend assets

### Security
- Implemented rate limiting for API endpoints
- Added command filtering to prevent exact answer disclosure
- Used environment variables for sensitive configuration
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Modern, clean UI design with professional appearance
- Chat-style mentor interface with welcome message
- Connection status indicator in header
- Enhanced terminal theme with custom colors
- WebSocket connection retry logic with exponential backoff
- Loading states and visual feedback for user interactions
- Responsive design for mobile devices
- Google Fonts integration (Inter + JetBrains Mono)
- Smooth animations and transitions throughout the interface
- Terminal focus management and auto-focus on page load
- Comprehensive improvement plan documentation

### Changed
- Complete UI redesign from Matrix-themed to modern clean interface
- Replaced simple sidebar with professional mentor panel
- Enhanced terminal with better error handling and reconnection
- Improved WebSocket protocol handling (ws/wss auto-detection)
- Updated mentor.js to use chat-style message display
- Modernized CSS with CSS custom properties and better organization

### Fixed
- WebSocket protocol mismatch (ws vs wss) causing connection failures
- Terminal not displaying bandit_title_screen.py output on app load
- Missing error handling for WebSocket disconnections
- Sidebar toggle and resize functionality
- Terminal fitting issues on window resize

### Security
- Improved WebSocket security with proper protocol detection
- Enhanced error handling to prevent information leakage

## [0.1.0] - 2025-01-20

### Added
- Initial BanditGUI implementation
- FastAPI backend with WebSocket support
- SSH connection to OverTheWire Bandit servers
- AI mentor system using Ollama/Qwen2.5:1.5b
- XTerm.js terminal emulation
- Rate limiting for AI mentor requests
- Command redaction to prevent cheating
- Basic Matrix-themed UI

### Technical Debt
- Limited error handling in WebSocket connections
- No session management
- Missing comprehensive documentation
- No automated testing
- Basic security measures only


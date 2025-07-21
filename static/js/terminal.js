import { FitAddon } from "https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/+esm";
import { Terminal } from "https://cdn.jsdelivr.net/npm/xterm@5.3.0/+esm";

const term = new Terminal({ 
  cursorBlink: true,
  theme: {
    background: '#0a0a0a',
    foreground: '#e6e6e6',
    cursor: '#00ff88',
    cursorAccent: '#0a0a0a',
    selection: 'rgba(0, 255, 136, 0.3)',
    black: '#0a0a0a',
    red: '#ff4757',
    green: '#00ff88',
    yellow: '#ffa502',
    blue: '#3742fa',
    magenta: '#ff6b9d',
    cyan: '#00d2d3',
    white: '#e6e6e6',
    brightBlack: '#333333',
    brightRed: '#ff6b9d',
    brightGreen: '#00ff88',
    brightYellow: '#ffa502',
    brightBlue: '#3742fa',
    brightMagenta: '#ff6b9d',
    brightCyan: '#00d2d3',
    brightWhite: '#ffffff'
  },
  fontSize: 14,
  fontFamily: 'JetBrains Mono, Courier New, monospace',
  lineHeight: 1.2,
  letterSpacing: 0.5,
  scrollback: 1000,
  allowTransparency: true
});

const fit = new FitAddon();
term.loadAddon(fit);
term.open(document.getElementById("terminal"));
fit.fit();

// Clear the terminal panel on main page load
term.clear();

// Connection status management
let isConnected = false;
let connectionAttempts = 0;
const maxRetries = 3;

function updateConnectionStatus(status, message) {
  const connectionStatus = document.getElementById('connectionStatus');
  if (connectionStatus) {
    const indicator = connectionStatus.querySelector('.status-indicator');
    const statusText = connectionStatus.querySelector('span');
    
    if (indicator) indicator.className = `status-indicator ${status}`;
    if (statusText) statusText.textContent = message;
  }
}

function connectWebSocket() {
  const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const ws = new WebSocket(`${protocol}//${location.host}/pty`);
  
  ws.onopen = () => {
    console.log('WebSocket connected');
    isConnected = true;
    connectionAttempts = 0;
    updateConnectionStatus('connected', 'Connected');
    
    // Send special message to backend to show the title screen
    ws.send('__SHOW_TITLE__');
  };
  
  ws.onmessage = (e) => {
    term.write(e.data);
  };
  
  ws.onclose = (e) => {
    console.log('WebSocket disconnected:', e.code, e.reason);
    isConnected = false;
    updateConnectionStatus('disconnected', 'Disconnected');
    
    // Attempt to reconnect
    if (connectionAttempts < maxRetries) {
      connectionAttempts++;
      updateConnectionStatus('connecting', `Reconnecting... (${connectionAttempts}/${maxRetries})`);
      setTimeout(() => connectWebSocket(), 2000 * connectionAttempts);
    } else {
      updateConnectionStatus('disconnected', 'Connection failed');
      term.write('\r\n\x1b[31mConnection lost. Please refresh the page to reconnect.\x1b[0m\r\n');
    }
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    updateConnectionStatus('disconnected', 'Connection error');
  };
  
  term.onData((data) => {
    if (isConnected) {
      ws.send(data);
    }
  });
  
  return ws;
}

// Initialize WebSocket connection
const ws = connectWebSocket();

// Handle window resize
window.addEventListener("resize", () => {
  setTimeout(() => fit.fit(), 100);
});

// Make terminal and fit available globally
window.term = term;
window.fit = fit;

// Terminal focus management
const terminalContainer = document.getElementById("terminal");
if (terminalContainer) {
  terminalContainer.addEventListener('click', () => {
    term.focus();
  });
}

// Auto-focus terminal on page load
setTimeout(() => {
  term.focus();
}, 500);
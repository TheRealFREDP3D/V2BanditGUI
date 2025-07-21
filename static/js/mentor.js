const askBtn = document.getElementById("askBtn");
const chatOutput = document.getElementById("chatOutput");
const connectionStatus = document.getElementById("connectionStatus");
let history = "";
let lastPrompt = "";
const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const resizeHandle = document.getElementById("resizeHandle");
const mainContent = document.querySelector(".main-content");

// Update connection status
function updateConnectionStatus(status, text) {
  const indicator = connectionStatus.querySelector('.status-indicator');
  const statusText = connectionStatus.querySelector('span');
  
  indicator.className = `status-indicator ${status}`;
  statusText.textContent = text;
}

// Add message to chat
function addMessage(author, text, isUser = false) {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'chat-message';
  
  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  avatar.textContent = isUser ? '👤' : '🤖';
  
  const content = document.createElement('div');
  content.className = 'message-content';
  
  const header = document.createElement('div');
  header.className = 'message-header';
  
  const authorSpan = document.createElement('span');
  authorSpan.className = 'message-author';
  authorSpan.textContent = author;
  
  const timeSpan = document.createElement('span');
  timeSpan.className = 'message-time';
  timeSpan.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  const messageText = document.createElement('div');
  messageText.className = 'message-text';
  messageText.innerHTML = text.replace(/\n/g, '<br>');
  
  header.appendChild(authorSpan);
  header.appendChild(timeSpan);
  content.appendChild(header);
  content.appendChild(messageText);
  messageDiv.appendChild(avatar);
  messageDiv.appendChild(content);
  
  chatOutput.appendChild(messageDiv);
  chatOutput.scrollTop = chatOutput.scrollHeight;
}

function capturePrompt() {
  // crude: last 20 lines of visible buffer
  const buffer = term.buffer.active;
  const lines = [];
  for (let i = Math.max(0, buffer.length - 20); i < buffer.length; i++) {
    lines.push(buffer.getLine(i)?.translateToString(true) || "");
  }
  history = lines.join("\n");
  const match = history.match(/bandit(\d+)@/);
  return match ? `bandit${match[1]}` : "bandit0";
}

// Enable ask button when terminal has data
if (typeof term !== 'undefined') {
  term.onData(() => {
    askBtn.disabled = false;
    updateConnectionStatus('connected', 'Connected');
  });
}

askBtn.onclick = async () => {
  askBtn.disabled = true;
  askBtn.innerHTML = `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="loading">
      <path d="M21 12a9 9 0 11-6.219-8.56"/>
    </svg>
    Thinking...
  `;
  
  const level = capturePrompt();
  
  try {
    const res = await fetch("/ask-a-pro", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ level, history }),
    });
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    
    const json = await res.json();
    addMessage("Neo", json.advice);
    
  } catch (error) {
    addMessage("Neo", `Sorry, I encountered an error: ${error.message}. Please try again later.`);
  } finally {
    askBtn.disabled = false;
    askBtn.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
      Ask Mentor
      <span class="shortcut">Ctrl+M</span>
    `;
  }
};

document.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "m") {
    e.preventDefault();
    askBtn.click();
  }
});

// Sidebar toggle logic
sidebarToggle.addEventListener("click", () => {
  mainContent.classList.toggle("sidebar-collapsed");
  sidebar.classList.toggle("collapsed");
  
  // Fit terminal after sidebar toggle
  setTimeout(() => {
    if (window.term && window.fit) {
      window.fit.fit();
    }
  }, 300);
});

// Drag handle logic for desktop
let isDragging = false;
let startX = 0;
let startWidth = 0;

resizeHandle.addEventListener("mousedown", (e) => {
  isDragging = true;
  startX = e.clientX;
  startWidth = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sidebar-width")) || 380;
  document.body.style.cursor = "col-resize";
  document.body.style.userSelect = "none";
  e.preventDefault();
});

document.addEventListener("mousemove", (e) => {
  if (!isDragging) return;
  
  const deltaX = e.clientX - startX;
  const newWidth = Math.max(280, Math.min(600, startWidth + deltaX));
  
  document.documentElement.style.setProperty("--sidebar-width", `${newWidth}px`);
});

document.addEventListener("mouseup", () => {
  if (isDragging) {
    isDragging = false;
    document.body.style.cursor = "";
    document.body.style.userSelect = "";
    
    // Fit terminal after resize
    setTimeout(() => {
      if (window.term && window.fit) {
        window.fit.fit();
      }
    }, 100);
  }
});

// Accessibility: keyboard resize
resizeHandle.addEventListener("keydown", (e) => {
  let current = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sidebar-width")) || 380;
  
  if (e.key === "ArrowLeft") {
    current = Math.max(280, current - 20);
    document.documentElement.style.setProperty("--sidebar-width", `${current}px`);
    if (window.term && window.fit) window.fit.fit();
    e.preventDefault();
  } else if (e.key === "ArrowRight") {
    current = Math.min(600, current + 20);
    document.documentElement.style.setProperty("--sidebar-width", `${current}px`);
    if (window.term && window.fit) window.fit.fit();
    e.preventDefault();
  }
});

// Mobile sidebar toggle
if (window.innerWidth <= 768) {
  sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("open");
  });
  
  // Close sidebar when clicking outside on mobile
  document.addEventListener("click", (e) => {
    if (window.innerWidth <= 768 && 
        !sidebar.contains(e.target) && 
        !sidebarToggle.contains(e.target) &&
        sidebar.classList.contains("open")) {
      sidebar.classList.remove("open");
    }
  });
}

// Initialize connection status
updateConnectionStatus('connecting', 'Connecting...');
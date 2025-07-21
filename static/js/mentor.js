const askBtn = document.getElementById("askBtn");
const advice = document.getElementById("advice");
let history = "";
let lastPrompt = "";
const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const dragHandle = document.getElementById("drag-handle");

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

term.onData(() => {
  askBtn.disabled = false;
});

askBtn.onclick = async () => {
  askBtn.disabled = true;
  const level = capturePrompt();
  const res = await fetch("/ask-a-pro", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ level, history }),
  });
  const json = await res.json();
  advice.textContent = json.advice;
};

document.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "m") askBtn.click();
});

// Sidebar toggle logic
sidebarToggle.addEventListener("click", () => {
  sidebar.classList.toggle("collapsed");
  if (sidebar.classList.contains("collapsed")) {
    document.documentElement.style.setProperty("--sidebar-width", "40px");
  } else {
    document.documentElement.style.setProperty("--sidebar-width", "300px");
  }
  resizeAndFitTerminal();
});

// Function to resize sidebar and fit terminal
function resizeAndFitTerminal(newWidth) {
  if (newWidth) {
    document.documentElement.style.setProperty("--sidebar-width", `${newWidth}px`);
  }
  if (window.term && window.term._core && window.fit) window.fit.fit();
}

// Drag handle logic
let isDragging = false;
dragHandle.addEventListener("mousedown", (e) => {
  isDragging = true;
  document.body.style.cursor = "col-resize";
});
document.addEventListener("mousemove", (e) => {
  if (!isDragging) return;
  const min = 40;
  const max = window.innerWidth - 100;
  let newWidth = e.clientX;
  if (newWidth < min) newWidth = min;
  if (newWidth > max) newWidth = max;
  resizeAndFitTerminal(newWidth);
});
document.addEventListener("mouseup", () => {
  if (isDragging) {
    isDragging = false;
    document.body.style.cursor = "";
  }
});
// Accessibility: keyboard resize
let handleFocused = false;
dragHandle.addEventListener("focus", () => { handleFocused = true; });
dragHandle.addEventListener("blur", () => { handleFocused = false; });
dragHandle.addEventListener("keydown", (e) => {
  if (!handleFocused) return;
  let current = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sidebar-width")) || 300;
  if (e.key === "ArrowLeft") {
    current = Math.max(40, current - 20);
    resizeAndFitTerminal(current);
    e.preventDefault();
  } else if (e.key === "ArrowRight") {

    current = Math.min(window.innerWidth - 100, current + 20);
    resizeAndFitTerminal(current);
    e.preventDefault();
  }
});
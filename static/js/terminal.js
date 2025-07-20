import { FitAddon } from "https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/+esm";
import { Terminal } from "https://cdn.jsdelivr.net/npm/xterm@5.3.0/+esm";

const term = new Terminal({ cursorBlink: true });
const fit = new FitAddon();
term.loadAddon(fit);
term.open(document.getElementById("terminal"));
fit.fit();
term.clear(); // Clear the terminal panel on main page load

const wsProtocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
const ws = new WebSocket(`${wsProtocol}${location.host}/pty`);
ws.onopen = () => {};
ws.onmessage = (e) => term.write(e.data);
term.onData((d) => ws.send(d));

// Send special message to backend to show the title screen
ws.addEventListener('open', () => {
  ws.send('__SHOW_TITLE__');
});

window.addEventListener("resize", () => fit.fit());
window.term = term;
window.fit = fit;
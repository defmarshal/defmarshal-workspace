// MewChat — main application logic with typewriter effects and mascot animations

(function() {
  'use strict';

  const { API_BASE, POLL_INTERVAL } = window.MewChatConfig;

  // State
  let currentSessionKey = localStorage.getItem('mewchat-session') || '';
  let pollTimer = null;
  let lastMessageCount = 0;

  // DOM refs
  const themeBtn = document.getElementById('theme-btn');
  const sessionSelect = document.getElementById('session-select');
  const chatMessages = document.getElementById('chat-messages');
  const msgInput = document.getElementById('msg-input');
  const sendBtn = document.getElementById('send-btn');
  const clearBtn = document.getElementById('clear-btn');
  const typingEl = document.getElementById('typing');
  const errorEl = document.getElementById('error');
  const mascot = document.getElementById('mascot');

  // Theme toggle
  function applyTheme() {
    const theme = localStorage.getItem('mewchat-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    themeBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
  }
  themeBtn.addEventListener('click', () => {
    const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    localStorage.setItem('mewchat-theme', newTheme);
    applyTheme();
  });
  applyTheme();

  // Helpers
  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function formatTime(ts) {
    const d = new Date(ts * 1000);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  // Typewriter effect: reveal text letter by letter
  function typewriterEffect(element, text, speed = 30) {
    element.textContent = '';
    element.classList.add('typewriter');
    let i = 0;
    function type() {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
        // scroll to bottom
        const chat = document.getElementById('chat-messages');
        if (chat) chat.scrollTop = chat.scrollHeight;
        setTimeout(type, speed);
      } else {
        element.classList.remove('typewriter');
      }
    }
    type();
  }

  // UI renderers
  function renderMessage(role, text, time, animate = false) {
    const div = document.createElement('div');
    div.className = 'msg ' + role;
    const avatar = role === 'assistant' ? '🐱' : '👤';
    div.innerHTML = `
      <div class="msg-row">
        <div class="msg-avatar">${avatar}</div>
        <div>
          <div class="msg-bubble"></div>
          <div class="msg-meta">${formatTime(time)}</div>
        </div>
      </div>
    `;
    chatMessages.appendChild(div);
    const bubble = div.querySelector('.msg-bubble');

    if (role === 'assistant' && animate) {
      // Typewriter effect for assistant messages
      typewriterEffect(bubble, text, 25);
      // Mascot talking animation
      if (mascot) {
        mascot.classList.add('talking');
        // Stop animation after approx duration of text
        const duration = Math.min(Math.max(text.length * 25, 500), 10000);
        setTimeout(() => mascot.classList.remove('talking'), duration);
      }
    } else {
      bubble.textContent = text;
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.classList.remove('hidden');
  }

  function clearError() {
    errorEl.classList.add('hidden');
  }

  function clearChat() {
    if (confirm('Clear the current chat history? This cannot be undone.')) {
      chatMessages.innerHTML = '';
      lastMessageCount = 0;
      // Optional: call API to clear on server? For now just local.
    }
  }

  // Data fetching
  async function loadSessions() {
    try {
      const res = await fetch(API_BASE + '/api/sessions');
      if (!res.ok) throw new Error('Failed to fetch sessions (HTTP ' + res.status + ')');
      const data = await res.json();
      sessionSelect.innerHTML = '';
      data.sessions.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.sessionKey;
        opt.textContent = s.label;
        sessionSelect.appendChild(opt);
      });
      if (data.sessions.length === 0) {
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = 'No sessions available';
        sessionSelect.disabled = true;
        return;
      }
      sessionSelect.disabled = false;
      if (currentSessionKey && data.sessions.some(s => s.sessionKey === currentSessionKey)) {
        sessionSelect.value = currentSessionKey;
      } else {
        currentSessionKey = data.sessions[0].sessionKey;
        sessionSelect.value = currentSessionKey;
        localStorage.setItem('mewchat-session', currentSessionKey);
      }
      await fetchChat();
    } catch (e) {
      showError('Could not load sessions: ' + e.message);
      sessionSelect.innerHTML = '<option value="">(error)</option>';
    }
  }

  async function fetchChat() {
    if (!currentSessionKey) return;
    try {
      const res = await fetch(API_BASE + '/api/chat?sessionKey=' + encodeURIComponent(currentSessionKey));
      if (!res.ok) throw new Error('Failed to fetch chat (HTTP ' + res.status + ')');
      const data = await res.json();
      chatMessages.innerHTML = '';
      lastMessageCount = 0;
      data.chat.forEach((m, idx) => {
        // Only animate the latest assistant message if it's new
        const isLatest = idx === data.chat.length - 1;
        const animate = m.role === 'assistant' && isLatest;
        renderMessage(m.role, m.text, m.ts, animate);
      });
      lastMessageCount = data.chat.length;
    } catch (e) {
      showError('Could not load chat: ' + e.message);
    }
  }

  async function sendMessage() {
    const text = msgInput.value.trim();
    if (!text || !currentSessionKey) return;
    msgInput.value = '';
    sendBtn.disabled = true;
    sendBtn.classList.add('loading');
    sendBtn.textContent = 'Sending…';
    typingEl.classList.remove('hidden');
    if (mascot) mascot.classList.add('talking');
    clearError();
    try {
      const res = await fetch(API_BASE + '/api/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, sessionKey: currentSessionKey })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to send');
      renderMessage('user', text, Date.now() / 1000, false);
    } catch (e) {
      showError('Send failed: ' + e.message);
    } finally {
      sendBtn.disabled = false;
      sendBtn.classList.remove('loading');
      sendBtn.textContent = 'Send';
      typingEl.classList.add('hidden');
      if (mascot) mascot.classList.remove('talking');
    }
  }

  // Polling for new replies
  function startPolling() {
    stopPolling();
    pollTimer = setInterval(async () => {
      if (!currentSessionKey) return;
      try {
        const res = await fetch(API_BASE + '/api/chat?sessionKey=' + encodeURIComponent(currentSessionKey));
        if (!res.ok) return;
        const data = await res.json();
        if (data.chat.length > lastMessageCount) {
          // New messages arrived
          const newMsgs = data.chat.slice(lastMessageCount);
          newMsgs.forEach((m, idx) => {
            const isLatest = idx === newMsgs.length - 1;
            const animate = m.role === 'assistant' && isLatest;
            renderMessage(m.role, m.text, m.ts, animate);
          });
          lastMessageCount = data.chat.length;
        }
      } catch (e) {
        // Silently ignore poll errors
      }
    }, POLL_INTERVAL);
  }

  function stopPolling() {
    if (pollTimer) clearInterval(pollTimer);
  }

  // Event listeners
  sessionSelect.addEventListener('change', () => {
    currentSessionKey = sessionSelect.value;
    localStorage.setItem('mewchat-session', currentSessionKey);
    fetchChat();
  });

  msgInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
  sendBtn.addEventListener('click', sendMessage);

  // Keyboard shortcuts
  document.addEventListener('keydown', e => {
    // Check for Ctrl/Cmd key combos
    const isMod = e.ctrlKey || e.metaKey;
    if (!isMod) return;

    switch (e.key.toLowerCase()) {
      case ',':
        e.preventDefault();
        themeBtn.click();
        break;
      case '/':
        e.preventDefault();
        msgInput.focus();
        break;
      case 'k':
        e.preventDefault();
        clearChat();
        break;
    }
  });

  // Clear button
  if (clearBtn) {
    clearBtn.addEventListener('click', clearChat);
  }

  // Initialize
  loadSessions().then(() => {
    startPolling();
  });
})();

// MewChat — main application logic with typewriter effects and mascot animations

(function() {
  'use strict';

  const { API_BASE, POLL_INTERVAL } = window.MewChatConfig;

  // State
  let currentSessionKey = localStorage.getItem('mewchat-session') || '';
  let pollTimer = null;
  let lastMessageCount = 0;
  let lastFailedMessage = null; // for retry
  let unreadCount = 0; // for title badge when tab hidden

  // Dom refs
  const themeBtn = document.getElementById('theme-btn');
  const sessionSelect = document.getElementById('session-select');
  const chatMessages = document.getElementById('chat-messages');
  const scrollBottomBtn = document.getElementById('scroll-bottom');
  const connectionStatus = document.getElementById('connection-status');
  const helpBtn = document.getElementById('help-btn');
  const helpModal = document.getElementById('help-modal');
  const helpClose = document.getElementById('help-close');
  const confirmModal = document.getElementById('confirm-modal');
  const confirmCancel = document.getElementById('confirm-cancel');
  const confirmOk = document.getElementById('confirm-ok');
  const msgInput = document.getElementById('msg-input');
  const sendBtn = document.getElementById('send-btn');
  const clearBtn = document.getElementById('clear-btn');
  const typingEl = document.getElementById('typing');
  const errorEl = document.getElementById('error');
  const mascot = document.getElementById('mascot');
  const charCountEl = document.getElementById('char-count');
  if (charCountEl) charCountEl.textContent = msgInput.value.length;

  // Connection status indicator
  function updateConnectionStatus() {
    const online = navigator.onLine;
    if (connectionStatus) {
      connectionStatus.classList.remove('online', 'offline');
      connectionStatus.classList.add(online ? 'online' : 'offline');
    }
  }
  window.addEventListener('online', updateConnectionStatus);
  window.addEventListener('offline', updateConnectionStatus);
  updateConnectionStatus(); // initial

  // Unread badge: reset title when tab becomes visible
  function resetTitleBadge() {
    if (unreadCount > 0) {
      unreadCount = 0;
      document.title = 'MewChat — chat with mewmew';
    }
  }
  window.addEventListener('visibilitychange', () => {
    if (!document.hidden) resetTitleBadge();
  });

  // Restore draft from localStorage (if any)
  const savedDraft = localStorage.getItem('mewchat-draft');
  if (savedDraft) {
    msgInput.value = savedDraft;
    // Update height and char count
    msgInput.style.height = 'auto';
    msgInput.style.height = Math.min(msgInput.scrollHeight, 150) + 'px';
    if (charCountEl) charCountEl.textContent = savedDraft.length;
    if (sendBtn && savedDraft.trim().length > 0) sendBtn.classList.add('has-text');
  }

  // Show/hide scroll-to-bottom button based on scroll position
  function toggleScrollBottomBtn() {
    if (!scrollBottomBtn) return;
    const atBottom = chatMessages.scrollHeight - chatMessages.scrollTop <= chatMessages.clientHeight + 10;
    if (atBottom) {
      scrollBottomBtn.classList.add('hidden');
    } else {
      scrollBottomBtn.classList.remove('hidden');
    }
  }

  chatMessages.addEventListener('scroll', toggleScrollBottomBtn);

  if (scrollBottomBtn) {
    scrollBottomBtn.addEventListener('click', () => {
      chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
    });
  }

  // Auto-resize textarea on input AND update character count + save draft
  msgInput.addEventListener('input', function() {
    this.style.height = 'auto';
    const newHeight = Math.min(this.scrollHeight, 150); // max-height: 150px
    this.style.height = newHeight + 'px';
    // Update character counter
    if (charCountEl) charCountEl.textContent = this.value.length;
    // Toggle pulse on send button if it has focus
    if (sendBtn) {
      if (this.value.trim().length > 0) sendBtn.classList.add('has-text');
      else sendBtn.classList.remove('has-text');
    }
    // Save draft to localStorage
    localStorage.setItem('mewchat-draft', this.value);
  });

  // Keyboard shortcuts: Ctrl+Enter to send, Escape to clear
  msgInput.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      clearChat();
    }
  });

  // Theme toggle
  function applyTheme() {
    let theme = localStorage.getItem('mewchat-theme');
    if (!theme) {
      // Match system preference when no explicit choice is stored
      theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    document.documentElement.setAttribute('data-theme', theme);
    themeBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
  }

  // Listen for system theme changes if user hasn't set a preference
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (!localStorage.getItem('mewchat-theme')) {
      applyTheme();
    }
  });

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
    showConfirmModal();
  }

  function showConfirmModal() {
    if (confirmModal) confirmModal.classList.remove('hidden');
  }
  function hideConfirmModal() {
    if (confirmModal) confirmModal.classList.add('hidden');
  }
  function performClear() {
    chatMessages.innerHTML = '';
    lastMessageCount = 0;
    localStorage.removeItem('mewchat-draft');
    msgInput.value = '';
    if (charCountEl) charCountEl.textContent = '0';
    msgInput.style.height = 'auto';
    hideConfirmModal();
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

  async function sendMessage(textOverride = null) {
    const text = textOverride || msgInput.value.trim();
    if (!text || !currentSessionKey) return;
    if (!textOverride) msgInput.value = '';
    const originalBtnText = sendBtn.textContent;
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
      lastFailedMessage = null;
      // Clear draft after successful send
      localStorage.removeItem('mewchat-draft');
    } catch (e) {
      lastFailedMessage = text;
      showError('Send failed: ' + e.message + ' <button class="retry-btn">Retry</button>');
      // Attach retry handler
      const retryBtn = errorEl.querySelector('.retry-btn');
      if (retryBtn) {
        retryBtn.addEventListener('click', () => {
          sendMessage(lastFailedMessage);
        });
      }
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
          const newMsgCount = data.chat.length - lastMessageCount;
          // Update unread badge if tab is hidden
          if (document.hidden) {
            unreadCount += newMsgCount;
            document.title = `(${unreadCount}) MewChat — chat with mewmew`;
          }
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
      case '1': case '2': case '3': case '4': case '5':
      case '6': case '7': case '8': case '9':
        e.preventDefault();
        const index = parseInt(e.key) - 1;
        if (sessionSelect.options.length > index) {
          sessionSelect.value = sessionSelect.options[index].value;
          sessionSelect.dispatchEvent(new Event('change'));
        }
        break;
    }
  });

  // Clear button
  if (clearBtn) {
    clearBtn.addEventListener('click', clearChat);
  }

  // Help modal
  function showHelp() {
    if (helpModal) helpModal.classList.remove('hidden');
  }
  function hideHelp() {
    if (helpModal) helpModal.classList.add('hidden');
  }
  if (helpBtn) helpBtn.addEventListener('click', showHelp);
  if (helpClose) helpClose.addEventListener('click', hideHelp);
  // Close modal when clicking on overlay (outside content)
  if (helpModal) {
    helpModal.addEventListener('click', e => {
      if (e.target === helpModal) hideHelp();
    });
  }
  // Close modal on Escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && helpModal && !helpModal.classList.contains('hidden')) {
      hideHelp();
    }
  });
  // Ctrl+H to toggle help
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'h') {
      e.preventDefault();
      if (helpModal && helpModal.classList.contains('hidden')) showHelp(); else hideHelp();
    }
  });

  // Confirm modal handlers
  if (confirmCancel) confirmCancel.addEventListener('click', hideConfirmModal);
  if (confirmOk) confirmOk.addEventListener('click', performClear);
  if (confirmModal) {
    confirmModal.addEventListener('click', e => {
      if (e.target === confirmModal) hideConfirmModal();
    });
  }
  // Also close confirm modal on Escape (global listener already handles help only; need separate check)
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if (helpModal && !helpModal.classList.contains('hidden')) hideHelp();
      if (confirmModal && !confirmModal.classList.contains('hidden')) hideConfirmModal();
    }
  });

  // Initialize
  loadSessions().then(() => {
    startPolling();
  });
})();

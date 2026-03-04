// MewChat — main application logic with typewriter effects and mascot animations

(function() {
  'use strict';

  const { API_BASE } = window.MewChatConfig;

  // State
  let currentSessionKey = localStorage.getItem('mewchat-session') || '';
  let sse = null;
  let lastMessageCount = 0;
  let lastFailedMessage = null; // for retry
  let unreadCount = 0; // for title badge when tab hidden
  let reconnectAttempts = 0;
  let reconnectTimeout = null;
  let reconnectSystemMessageId = null; // track system message for updates
  const RECONNECT_BASE = 1000; // 1 second
  const RECONNECT_MAX = 30000; // 30 seconds
  const RECONNECT_MAX_ATTEMPTS = 10; // give up after ~30 mins if no success

  // Dom refs
  const themeBtn = document.getElementById('theme-btn');
  const settingsBtn = document.getElementById('settings-btn');
  const sessionSelect = document.getElementById('session-select');
  const chatMessages = document.getElementById('chat-messages');
  const scrollBottomBtn = document.getElementById('scroll-bottom');
  const connectionStatus = document.getElementById('connection-status');
  const lastUpdatedEl = document.getElementById('last-updated');
  const helpBtn = document.getElementById('help-btn');
  const helpModal = document.getElementById('help-modal');
  const helpClose = document.getElementById('help-close');
  const settingsModal = document.getElementById('settings-modal');
  const settingsClose = document.getElementById('settings-close');
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
    updateCharCountAndCheckLimit();
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
    // Update character counter with limit warning
    updateCharCountAndCheckLimit();
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

  function formatRelativeTime(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds
    if (diff < 60) return 'just now';
    const minutes = Math.floor(diff / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  }

  let lastUpdateTime = null;
  function updateLastUpdated() {
    if (!lastUpdatedEl) return;
    const now = new Date();
    lastUpdateTime = now;
    lastUpdatedEl.textContent = `Updated ${formatRelativeTime(now)}`;
  }

  // Reconnection status messages
  function showReconnectStatus() {
    removeReconnectStatus(); // remove any existing
    const msg = `Connection lost. Reconnecting… (attempt ${reconnectAttempts})`;
    const div = document.createElement('div');
    div.className = 'msg system';
    div.id = 'reconnect-status';
    div.innerHTML = `
      <div class="msg-bubble" style="text-align:center; color:var(--yellow); font-size:12px;">
        ⚠️ ${msg}
      </div>
    `;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function removeReconnectStatus() {
    const existing = document.getElementById('reconnect-status');
    if (existing) existing.remove();
  }

  function showReconnectSuccess() {
    removeReconnectStatus();
    const div = document.createElement('div');
    div.className = 'msg system';
    div.innerHTML = `
      <div class="msg-bubble" style="text-align:center; color:var(--green); font-size:12px;">
        ✅ Reconnected successfully
      </div>
    `;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    // Auto-remove after 3 seconds
    setTimeout(() => div.remove(), 3000);
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

  function renderMessage(role, text, time, animate = false) {
    const div = document.createElement('div');
    div.className = 'msg ' + role;
    const avatar = role === 'assistant' ? `<svg viewBox="0 0 100 100" width="24" height="24" style="vertical-align:middle"><g transform="translate(0,-10)"><circle cx="50" cy="60" r="40" fill="#ff79c6" stroke="#ffb86c" stroke-width="3"/><polygon points="20,35 30,50 10,50" fill="#ff79c6" stroke="#ffb86c" stroke-width="2"/><polygon points="80,35 70,50 90,50" fill="#ff79c6" stroke="#ffb86c" stroke-width="2"/><polygon points="22,42 28,50 15,50" fill="#ffb86c"/><polygon points="78,42 72,50 85,50" fill="#ffb86c"/><ellipse cx="38" cy="55" rx="5" ry="7" fill="#0b0e14"/><ellipse cx="62" cy="55" rx="5" ry="7" fill="#0b0e14"/><ellipse cx="50" cy="50" rx="6" ry="4" fill="#0b0e14"/><ellipse cx="30" cy="70" rx="8" ry="5" fill="#ff6b9d" opacity="0.6"/><ellipse cx="70" cy="70" rx="8" ry="5" fill="#ff6b9d" opacity="0.6"/><path d="M 40 75 Q 50 82 60 75" stroke="#0b0e14" stroke-width="3" fill="none" stroke-linecap="round"/><line x1="15" y1="60" x2="30" y2="65" stroke="#0b0e14" stroke-width="2"/><line x1="15" y1="70" x2="30" y2="70" stroke="#0b0e14" stroke-width="2"/><line x1="85" y1="60" x2="70" y2="65" stroke="#0b0e14" stroke-width="2"/><line x1="85" y1="70" x2="70" y2="70" stroke="#0b0e14" stroke-width="2"/><circle cx="85" cy="85" r="8" fill="#ff79c6" stroke="#ffb86c" stroke-width="2"/></g></svg>` : '👤';
    div.innerHTML = `
      <div class="msg-row">
        <div class="msg-avatar">${avatar}</div>
        <div>
          <div class="msg-bubble"></div>
          ${role === 'assistant' ? '<button class="msg-copy-btn" title="Copy to clipboard">📋</button>' : ''}
          <div class="msg-meta">${formatTime(time)}</div>
        </div>
      </div>
    `;
    chatMessages.appendChild(div);
    const bubble = div.querySelector('.msg-bubble');
    const copyBtn = div.querySelector('.msg-copy-btn');

    if (copyBtn) {
      copyBtn.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(text);
          copyBtn.classList.add('copied');
          copyBtn.title = 'Copied!';
          setTimeout(() => {
            copyBtn.classList.remove('copied');
            copyBtn.title = 'Copy to clipboard';
          }, 1500);
        } catch (err) {
          console.error('Copy failed:', err);
          copyBtn.title = 'Copy failed';
        }
      });
    }

    if (role === 'assistant' && animate) {
      const settings = loadSettings();
      if (settings.typewriterEnabled) {
        typewriterEffect(bubble, text, settings.typewriterSpeed);
      } else {
        bubble.textContent = text;
      }
      if (settings.mascotAnimation && mascot && settings.typewriterEnabled) {
        mascot.classList.add('talking');
        const duration = Math.min(Math.max(text.length * settings.typewriterSpeed, 500), 10000);
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

  // Copy full chat history to clipboard
  async function copyChatHistory() {
    const messages = chatMessages.querySelectorAll('.msg');
    if (messages.length === 0) {
      showError('Chat is empty — nothing to copy.');
      setTimeout(() => clearError(), 3000);
      return;
    }

    let text = '=== MewChat History ===\n\n';
    messages.forEach(msg => {
      const role = msg.classList.contains('user') ? '👤 You' : '🤖 mewmew';
      const bubble = msg.querySelector('.msg-bubble');
      const meta = msg.querySelector('.msg-meta');
      const time = meta ? meta.textContent : '';
      const content = bubble ? bubble.textContent.trim() : '';
      text += `[${time}] ${role}:\n${content}\n\n`;
    });

    try {
      await navigator.clipboard.writeText(text);
      showError('✅ Chat history copied to clipboard!');
      // Change copy button temporarily to indicate success
      const copyBtn = document.getElementById('copy-chat-btn');
      if (copyBtn) {
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied';
        copyBtn.title = 'Copied!';
        setTimeout(() => {
          copyBtn.textContent = originalText;
          copyBtn.title = 'Copy full chat history to clipboard (Ctrl+Shift+C)';
        }, 2000);
      }
    } catch (err) {
      showError('Failed to copy: ' + err.message);
    }
    setTimeout(() => clearError(), 3000);
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
      startSSE(currentSessionKey);
    } catch (e) {
      showError('Could not load sessions: ' + e.message);
      sessionSelect.innerHTML = '<option value="">(error)</option>';
    }
  }

  // Deprecated: using SSE now

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
  function scheduleReconnect(sessionKey) {
    if (reconnectTimeout) clearTimeout(reconnectTimeout);

    // If we've exceeded max attempts, give up and show error
    if (reconnectAttempts >= RECONNECT_MAX_ATTEMPTS) {
      showError('Connection lost. Please reload the page or switch sessions to reconnect.');
      removeReconnectStatus();
      if (connectionStatus) connectionStatus.classList.add('offline');
      return;
    }

    // Calculate delay with exponential backoff (capped at MAX)
    const delay = Math.min(RECONNECT_BASE * Math.pow(2, reconnectAttempts), RECONNECT_MAX);
    reconnectAttempts++;

    // Show status message in chat
    showReconnectStatus();

    reconnectTimeout = setTimeout(() => {
      console.log(`[MewChat] Reconnection attempt ${reconnectAttempts} in ${delay}ms`);
      startSSE(sessionKey, true); // true = isReconnect
    }, delay);
  }

  function startSSE(sessionKey, isReconnect = false) {
    stopSSE();
    if (!sessionKey) return;

    sse = new EventSource(API_BASE + '/api/chat-stream?sessionKey=' + encodeURIComponent(sessionKey));

    sse.onopen = () => {
      if (connectionStatus) {
        connectionStatus.classList.remove('offline');
        connectionStatus.classList.add('online');
      }
      // Clear chat for fresh connection/reconnection
      lastMessageCount = 0;
      chatMessages.innerHTML = '';
      unreadCount = 0;
      document.title = 'MewChat — chat with mewmew';
      // Reset reconnection state on successful open
      reconnectAttempts = 0;
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
        reconnectTimeout = null;
      }
      // Remove any pending reconnect status and show success if this was a reconnection
      removeReconnectStatus();
      if (isReconnect) {
        showReconnectSuccess();
        console.log('[MewChat] Reconnected successfully');
      }
    };

    sse.onerror = () => {
      if (connectionStatus) connectionStatus.classList.add('offline');
      console.error('[MewChat] SSE error, scheduling reconnect...');
      // Schedule reconnection
      scheduleReconnect(sessionKey);
    };

    sse.onclose = () => {
      console.log('[MewChat] SSE closed');
      // If we didn't initiate the close (via stopSSE), attempt reconnect
      if (reconnectAttempts < RECONNECT_MAX_ATTEMPTS) {
        scheduleReconnect(sessionKey);
      }
    };

    sse.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (!data.chat) return;
        const newCount = data.chat.length;
        if (newCount > lastMessageCount) {
          const newMsgs = data.chat.slice(lastMessageCount);
          if (document.hidden) {
            unreadCount += newMsgs.length;
            document.title = `(${unreadCount}) MewChat — chat with mewmew`;
          }
          newMsgs.forEach((m, idx) => {
            const isLatest = idx === newMsgs.length - 1;
            const animate = m.role === 'assistant' && isLatest;
            renderMessage(m.role, m.text, m.ts, animate);
          });
          lastMessageCount = newCount;
          updateLastUpdated();
        }
      } catch (e) {
        console.error('SSE parse error:', e);
      }
    };
  }

  function stopSSE() {
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout);
      reconnectTimeout = null;
    }
    if (sse) {
      sse.close();
      sse = null;
    }
    reconnectAttempts = 0;
    removeReconnectStatus();
  }

  // Event listeners
  sessionSelect.addEventListener('change', () => {
    currentSessionKey = sessionSelect.value;
    localStorage.setItem('mewchat-session', currentSessionKey);
    startSSE(currentSessionKey);
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

    // Ctrl+Shift+C: Copy chat history
    if (e.shiftKey && e.key.toLowerCase() === 'c') {
      e.preventDefault();
      copyChatHistory();
      return;
    }

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

  // Copy chat history button
  const copyChatBtn = document.getElementById('copy-chat-btn');
  if (copyChatBtn) copyChatBtn.addEventListener('click', copyChatHistory);
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

  // Settings modal
  function showSettings() {
    if (settingsModal) {
      loadSettingsToModal();
      settingsModal.classList.remove('hidden');
    }
  }
  function hideSettings() {
    if (settingsModal) settingsModal.classList.add('hidden');
  }
  if (settingsBtn) settingsBtn.addEventListener('click', showSettings);
  if (settingsClose) settingsClose.addEventListener('click', hideSettings);
  if (settingsModal) {
    settingsModal.addEventListener('click', e => {
      if (e.target === settingsModal) hideSettings();
    });
  }
  // Ctrl+; to open settings
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === ';') {
      e.preventDefault();
      showSettings();
    }
  });
  // Escape closes settings modal too
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && settingsModal && !settingsModal.classList.contains('hidden')) {
      hideSettings();
    }
  });

  // Settings management
  const SETTINGS_KEYS = {
    TYPEWRITER_ENABLED: 'mewchat-typewriter-enabled',
    TYPEWRITER_SPEED: 'mewchat-typewriter-speed',
    MASCOT_ANIMATION: 'mewchat-mascot-animation',
    CHAR_LIMIT: 'mewchat-char-limit'
  };

  const DEFAULT_SETTINGS = {
    typewriterEnabled: true,
    typewriterSpeed: 25,
    mascotAnimation: true,
    charLimit: 0
  };

  function loadSettings() {
    const stored = {};
    for (const [key, storageKey] of Object.entries(SETTINGS_KEYS)) {
      const value = localStorage.getItem(storageKey);
      if (value !== null) {
        if (key.includes('SPEED') || key.includes('CHAR_LIMIT')) {
          stored[key] = parseInt(value, 10);
        } else if (key.includes('ENABLED') || key.includes('ANIMATION')) {
          stored[key] = value === 'true';
        } else {
          stored[key] = value;
        }
      }
    }
    return { ...DEFAULT_SETTINGS, ...stored };
  }

  function loadSettingsToModal() {
    const settings = loadSettings();
    const typewriterCheckbox = document.getElementById('setting-typewriter');
    const speedRadios = document.querySelectorAll('input[name="typewriter-speed"]');
    const mascotCheckbox = document.getElementById('setting-mascot');
    const charLimitSelect = document.getElementById('setting-charlimit');

    if (typewriterCheckbox) typewriterCheckbox.checked = settings.typewriterEnabled;
    for (const radio of speedRadios) {
      radio.checked = parseInt(radio.value, 10) === settings.typewriterSpeed;
    }
    if (mascotCheckbox) mascotCheckbox.checked = settings.mascotAnimation;
    if (charLimitSelect) charLimitSelect.value = settings.charLimit.toString();
  }

  function saveSettings() {
    const typewriterEnabled = document.getElementById('setting-typewriter')?.checked ?? DEFAULT_SETTINGS.typewriterEnabled;
    const speedRadio = document.querySelector('input[name="typewriter-speed"]:checked');
    const typewriterSpeed = speedRadio ? parseInt(speedRadio.value, 10) : DEFAULT_SETTINGS.typewriterSpeed;
    const mascotAnimation = document.getElementById('setting-mascot')?.checked ?? DEFAULT_SETTINGS.mascotAnimation;
    const charLimit = parseInt(document.getElementById('setting-charlimit')?.value ?? '0', 10);

    localStorage.setItem(SETTINGS_KEYS.TYPEWRITER_ENABLED, typewriterEnabled);
    localStorage.setItem(SETTINGS_KEYS.TYPEWRITER_SPEED, typewriterSpeed);
    localStorage.setItem(SETTINGS_KEYS.MASCOT_ANIMATION, mascotAnimation);
    localStorage.setItem(SETTINGS_KEYS.CHAR_LIMIT, charLimit);
    hideSettings();
  }

  function resetSettings() {
    for (const [key, storageKey] of Object.entries(SETTINGS_KEYS)) {
      localStorage.removeItem(storageKey);
    }
    loadSettingsToModal();
  }

  document.getElementById('settings-save')?.addEventListener('click', saveSettings);
  document.getElementById('settings-reset')?.addEventListener('click', resetSettings);

  // Character limit warning
  let charLimitWarningShown = false;
  function updateCharCountAndCheckLimit() {
    if (!charCountEl) return;
    const settings = loadSettings();
    const currentLength = msgInput.value.length;
    charCountEl.textContent = currentLength;

    if (settings.charLimit > 0 && currentLength >= settings.charLimit) {
      charCountEl.style.color = 'var(--red)';
      charCountEl.style.fontWeight = '700';
      if (!charLimitWarningShown) {
        charCountEl.textContent += ' (max reached)';
        charLimitWarningShown = true;
      }
    } else {
      charCountEl.style.color = '';
      charCountEl.style.fontWeight = '';
      charLimitWarningShown = false;
    }
  }

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
    startSSE(currentSessionKey);
  });
})();

// MewChat — main application logic with typewriter effects and mascot animations
// Enhanced with dashboard chat system features

(function() {
  'use strict';

  const { API_BASE } = window.MewChatConfig;

  // State
  let currentSessionKey = localStorage.getItem('mewchat-session') || '';
  let sse = null;
  let lastMessageCount = 0;
  let lastFailedMessage = null; // for retry
  let unreadCount = 0; // for title badge when tab hidden
  let unreadBannerCount = 0; // for new messages banner
  let reconnectAttempts = 0;
  let reconnectTimeout = null;
  let reconnectSystemMessageId = null; // track system message for updates
  const RECONNECT_BASE = 1000; // 1 second
  const RECONNECT_MAX = 30000; // 30 seconds
  const RECONNECT_MAX_ATTEMPTS = 10; // give up after ~30 mins if no success

  // Chat state (from dashboard)
  let chatData = []; // store all messages
  let chatSending = false; // suppress poll re-renders while message in flight
  let chatReplyWatcher = null; // for sendMessage reply polling
  let sseReconnectAttempts = 0;
  let sseReconnectTimer = null;
  const MAX_SSE_RECONNECT_ATTEMPTS = 10;
  const SSE_RECONNECT_DELAY = 3000; // 3 seconds

  // Dom refs
  const themeBtn = document.getElementById('theme-btn');
  const settingsBtn = document.getElementById('settings-btn');
  const sessionSelect = document.getElementById('session-select');
  const chatMessages = document.getElementById('chat-messages');
  const scrollBottomBtn = document.getElementById('scroll-bottom');
  const scrollTopBtn = document.getElementById('scroll-top');
  const clearInputBtn = document.getElementById('clear-input-btn');
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
  const notificationEl = document.getElementById('notification');
  const mascot = document.getElementById('mascot');
  const charCountEl = document.getElementById('char-count');
  const newMessagesBanner = document.getElementById('new-messages-banner');
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

  // Show/hide scroll-to-top button based on scroll position
  function toggleScrollTopBtn() {
    if (!scrollTopBtn) return;
    const atTop = chatMessages.scrollTop <= 10;
    if (atTop) {
      scrollTopBtn.classList.add('hidden');
    } else {
      scrollTopBtn.classList.remove('hidden');
    }
  }

  chatMessages.addEventListener('scroll', () => {
    toggleScrollBottomBtn();
    toggleScrollTopBtn();
    // Reset banner when scrolled to bottom
    if (isAtBottom()) {
      unreadBannerCount = 0;
      updateNewMessagesBanner();
    }
  });

  if (scrollBottomBtn) {
    scrollBottomBtn.addEventListener('click', () => {
      chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
    });
  }
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      chatMessages.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Clear input button
  if (clearInputBtn) {
    clearInputBtn.addEventListener('click', () => {
      msgInput.value = '';
      // Trigger input event to update height, char count, and toggle button
      msgInput.dispatchEvent(new Event('input'));
      msgInput.focus();
    });
    // Initial state
    clearInputBtn.classList.toggle('hidden', msgInput.value.length === 0);
  }

  // Auto-resize textarea on input AND update character count + save draft
  msgInput.addEventListener('input', function() {
    this.style.height = 'auto';
    const newHeight = Math.min(this.scrollHeight, 150); // max-height: 150px
    this.style.height = newHeight + 'px';
    
    // Update character counter
    const len = this.value.length;
    if (charCountEl) {
      charCountEl.textContent = len > 0 ? len + ' chars' : '';
      charCountEl.style.opacity = len > 200 ? '1' : '0.5';
      if (len > 500) {
        charCountEl.style.color = 'var(--error)';
        charCountEl.style.fontWeight = '700';
      } else {
        charCountEl.style.color = '';
        charCountEl.style.fontWeight = '';
      }
    }
    
    // Toggle pulse on send button if it has focus
    if (sendBtn) {
      if (this.value.trim().length > 0) sendBtn.classList.add('has-text');
      else sendBtn.classList.remove('has-text');
    }
    // Toggle clear input button visibility
    if (clearInputBtn) {
      clearInputBtn.classList.toggle('hidden', this.value.length === 0);
    }
    // Save draft to localStorage
    localStorage.setItem(getDraftKey(), this.value);
  });

  // Enhanced keyboard shortcuts from dashboard
  msgInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
    if (e.key === 'Escape') {
      msgInput.value = '';
      msgInput.style.height = 'auto';
      if (charCountEl) charCountEl.textContent = '0';
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

  function fmtTime(ts) {
    if (!ts) return '';
    try { return new Date(ts).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}); } catch { return ''; }
  }

  function timeAgo(ts) {
    if (!ts) return '';
    const d = typeof ts === 'number' ? new Date(ts * 1000) : new Date(ts);
    if (isNaN(d)) return ts;
    const s = Math.floor((Date.now() - d) / 1000);
    if (s < 60) return s + 's ago';
    if (s < 3600) return Math.floor(s/60) + 'm ago';
    if (s < 86400) return Math.floor(s/3600) + 'h ago';
    return Math.floor(s/86400) + 'd ago';
  }

  function esc(s) { return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }

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

  // Draft management per session
  function getDraftKey() {
    return `mewchat-draft-${currentSessionKey || 'default'}`;
  }

  function loadDraftForCurrentSession() {
    const draft = localStorage.getItem(getDraftKey()) || '';
    if (msgInput) {
      msgInput.value = draft;
      // Trigger input event to update height, char count, and toggle button
      msgInput.dispatchEvent(new Event('input'));
    }
  }

  // New Messages Banner helpers
  function isAtBottom() {
    return chatMessages.scrollHeight - chatMessages.scrollTop <= chatMessages.clientHeight + 10;
  }

  function updateNewMessagesBanner() {
    if (!newMessagesBanner) return;
    const countEl = newMessagesBanner.querySelector('.count');
    if (countEl) countEl.textContent = unreadBannerCount;
    if (unreadBannerCount > 0) {
      newMessagesBanner.classList.remove('hidden');
    } else {
      newMessagesBanner.classList.add('hidden');
    }
  }

  function onBannerClick() {
    chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
    unreadBannerCount = 0;
    updateNewMessagesBanner();
  }

  // Attach click handler for banner
  if (newMessagesBanner) {
    newMessagesBanner.addEventListener('click', onBannerClick);
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

  function showLoadingChat() {
    removeLoadingChat(); // remove any existing
    const div = document.createElement('div');
    div.className = 'msg system';
    div.id = 'loading-chat';
    div.innerHTML = `
      <div class="msg-bubble" style="text-align:center; color:var(--muted); font-size:12px;">
        <span class="typing-dots"><span></span><span></span><span></span></span> Loading chat…
      </div>
    `;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function removeLoadingChat() {
    const existing = document.getElementById('loading-chat');
    if (existing) existing.remove();
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

  function renderMessage(role, text, time, animate = false, autoScroll = true) {
    const div = document.createElement('div');
    div.className = 'msg ' + role;
    const avatar = role === 'assistant' ? `<svg viewBox="0 0 100 100" width="24" height="24" style="vertical-align:middle"><g transform="translate(0,-10)"><circle cx="50" cy="60" r="40" fill="#ff79c6" stroke="#ffb86c" stroke-width="3"/><polygon points="20,35 30,50 10,50" fill="#ff79c6" stroke="#ffb86c" stroke-width="2"/><polygon points="80,35 70,50 90,50" fill="#ff79c6" stroke="#ffb86c" stroke-width="2"/><polygon points="22,42 28,50 15,50" fill="#ffb86c"/><polygon points="78,42 72,50 85,50" fill="#ffb86c"/><ellipse cx="38" cy="55" rx="5" ry="7" fill="#0b0e14"/><ellipse cx="62" cy="55" rx="5" ry="7" fill="#0b0e14"/><ellipse cx="50" cy="50" rx="6" ry="4" fill="#0b0e14"/><ellipse cx="30" cy="70" rx="8" ry="5" fill="#ff6b9d" opacity="0.6"/><ellipse cx="70" cy="70" rx="8" ry="5" fill="#ff6b9d" opacity="0.6"/><path d="M 40 75 Q 50 82 60 75" stroke="#0b0e14" stroke-width="3" fill="none" stroke-linecap="round"/><line x1="15" y1="60" x2="30" y2="65" stroke="#0b0e14" stroke-width="2"/><line x1="15" y1="70" x2="30" y2="70" stroke="#0b0e14" stroke-width="2"/><line x1="85" y1="60" x2="70" y2="65" stroke="#0b0e14" stroke-width="2"/><line x1="85" y1="70" x2="70" y2="70" stroke="#0b0e14" stroke-width="2"/><circle cx="85" cy="85" r="8" fill="#ff79c6" stroke="#ffb86c" stroke-width="2"/></g></svg>` : '👤';
    div.innerHTML = `
      <div class="msg-row">
        <div class="msg-avatar">${avatar}</div>
        <div>
          <div class="msg-bubble"></div>
          ${(role === 'assistant' || role === 'user') ? '<button class="msg-copy-btn" title="Copy to clipboard">📋</button>' : ''}
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
    if (autoScroll) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    return div; // return element for status updates
  }

  // ── Enhanced renderChat from dashboard ──────────────────────────────────
  let lastChatLen = 0;

  function renderChat(messages, preserve_scroll = false) {
    chatData = messages || [];
    const container = chatMessages;

    // Save scroll position before re-render
    const scrollHeightBefore = container.scrollHeight;
    const scrollTopBefore = container.scrollTop;
    const clientHeightBefore = container.clientHeight;
    const atBottom = scrollHeightBefore - scrollTopBefore - clientHeightBefore < 60;

    if (!chatData.length) {
      container.innerHTML = '<div style="padding:32px 16px;text-align:center;color:var(--muted);font-size:13px">💬 No messages yet.<br><span style="font-size:11px">Send something below to start chatting with mewmew~</span></div>';
      return;
    }

    let lastDate = null;
    container.innerHTML = chatData.map(m => {
      const role = m.role === 'user' ? 'user' : 'assistant';
      const label = role === 'user' ? '👤 You' : '🐾 mewmew';
      let text = esc(m.text || '');

      // code blocks first (multiline)
      text = text.replace(/```[\s\S]*?```/g, b => {
        const code = b.slice(3, -3).replace(/^[a-z]+\n/, '');
        return '<pre style="background:#0a0d11;padding:8px;border-radius:6px;font-size:10px;overflow-x:auto;margin:4px 0;white-space:pre-wrap;color:#8b949e">' + esc(code) + '</pre>';
      });
      // bold
      text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
      // inline code
      text = text.replace(/`([^`\n]+)`/g, '<code style="background:#0a0d11;padding:1px 4px;border-radius:3px;font-size:10px;font-family:monospace">$1</code>');
      // newlines
      text = text.replace(/\n/g, '<br>');

      let sep = '';
      if (m.ts) {
        const d = new Date(m.ts).toLocaleDateString([], {weekday:'short', month:'short', day:'numeric'});
        if (d !== lastDate) {
          lastDate = d;
          sep = `<div style="text-align:center;font-size:10px;color:var(--muted);padding:8px 0;user-select:none">${d}</div>`;
        }
      }

      const avatar = role === 'assistant'
        ? `<div class="msg-avatar">🐾</div>`
        : `<div class="msg-avatar">👤</div>`;

      return sep + `<div class="msg ${role}" data-ts="${m.ts || ''}">
        <div class="msg-row">${avatar}<div class="msg-bubble">${text}</div></div>
        <div class="msg-meta">${label} · ${fmtTime(m.ts)}</div>
      </div>`;
    }).join('');

    // Restore scroll position intelligently
    if (preserve_scroll) {
      if (atBottom) {
        scrollChat();
      } else {
        const scrollHeightAfter = container.scrollHeight;
        const heightDiff = scrollHeightAfter - scrollHeightBefore;
        container.scrollTop = Math.max(0, scrollTopBefore + heightDiff);
      }
    } else {
      scrollChat();
    }

    const newTotal = chatData.length;
    if (lastChatLen > 0 && newTotal > lastChatLen) {
      const newest = chatData[chatData.length - 1];
      if (newest && newest.role !== 'user') {
        removeTypingIndicator();
        playPopSound();
      } else {
        removeTypingIndicator();
      }
    }
    lastChatLen = newTotal;
  }

  function scrollChat() {
    if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function showTypingIndicator() {
    removeTypingIndicator();
    const div = document.createElement('div');
    div.className = 'msg assistant typing';
    div.id = 'typing-indicator';
    div.innerHTML = `<div class="msg-bubble"><div class="typing-dots"><span></span><span></span><span></span></div></div><div class="msg-meta">🐾 mewmew is typing…</div>`;
    chatMessages.appendChild(div);
    scrollChat();
  }

  function removeTypingIndicator() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
  }

  // ── Sound effects ───────────────────────────────────────────────────────
  let _audioCtx = null;
  function getAudioCtx() {
    if (!_audioCtx || _audioCtx.state === 'closed') {
      _audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (_audioCtx.state === 'suspended') _audioCtx.resume();
    return _audioCtx;
  }
  document.addEventListener('click', () => { try { getAudioCtx(); } catch {} }, { once: true });
  document.addEventListener('keydown', () => { try { getAudioCtx(); } catch {} }, { once: true });

  function playPopSound() {
    try {
      const ctx = getAudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain); gain.connect(ctx.destination);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(1200, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(600, ctx.currentTime + 0.06);
      gain.gain.setValueAtTime(0.2, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + 0.12);
    } catch {}
  }

  function applyTimestampVisibility() {
    const settings = loadSettings();
    if (chatMessages) {
      if (settings.showTimestamps) {
        chatMessages.classList.remove('hide-timestamps');
      } else {
        chatMessages.classList.add('hide-timestamps');
      }
    }
  }

  function applyMascotVisibility() {
    const settings = loadSettings();
    const mascotEl = document.getElementById('mascot');
    if (mascotEl) {
      if (settings.showMascot) {
        mascotEl.style.display = '';
      } else {
        mascotEl.style.display = 'none';
      }
    }
  }

  function applySystemMessagesVisibility() {
    const settings = loadSettings();
    if (chatMessages) {
      if (settings.hideSystemMsgs) {
        chatMessages.classList.add('hide-system');
      } else {
        chatMessages.classList.remove('hide-system');
      }
    }
  }

  function showNotification(type, msg, duration = 5000) {
    removeLoadingChat(); // ensure loading indicator is gone
    if (!notificationEl) return;
    
    // Clear any existing notification
    hideNotification();
    
    notificationEl.innerHTML = `
      <span>${msg}</span>
      <button class="notification-dismiss" title="Dismiss">×</button>
    `;
    notificationEl.className = `notification ${type}`;
    notificationEl.classList.remove('hidden');
    
    // Add dismiss handler
    const dismissBtn = notificationEl.querySelector('.notification-dismiss');
    if (dismissBtn) {
      dismissBtn.addEventListener('click', hideNotification);
    }
    
    // Auto-dismiss after duration
    if (duration > 0) {
      setTimeout(hideNotification, duration);
    }
  }

  function hideNotification() {
    if (notificationEl) {
      notificationEl.classList.add('hidden');
      notificationEl.innerHTML = '';
      notificationEl.className = 'notification';
    }
  }

  // Backwards compatibility - now uses notification system
  function showError(msg) {
    showNotification('error', msg, 10000); // errors stay longer (10s)
  }

  function clearError() {
    hideNotification();
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
      showNotification('success', '✅ Chat history copied to clipboard!');
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

  function clearChat() {
    showConfirmModal();
  }

  function showConfirmModal() {
    const count = chatMessages.querySelectorAll('.msg').length;
    const desc = document.getElementById('confirm-desc');
    if (desc) {
      desc.textContent = count > 0
        ? `This will permanently delete ${count} message(s). This action cannot be undone.`
        : 'Chat is already empty.';
    }
    if (confirmModal) confirmModal.classList.remove('hidden');
  }
  function hideConfirmModal() {
    if (confirmModal) confirmModal.classList.add('hidden');
  }
  function performClear() {
    chatMessages.innerHTML = '';
    lastMessageCount = 0;
    unreadBannerCount = 0;
    updateNewMessagesBanner();
    localStorage.removeItem(getDraftKey());
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
      // Reset banner count on session load/switch
      unreadBannerCount = 0;
      updateNewMessagesBanner();
      startSSE(currentSessionKey);
      loadDraftForCurrentSession();
      // Cache session options for search filtering
      cacheSessionOptions();
      // Clear search input to show all sessions after load
      const sessionSearch = document.getElementById('session-search');
      if (sessionSearch) sessionSearch.value = '';
    } catch (e) {
      showError('Could not load sessions: ' + e.message);
      sessionSelect.innerHTML = '<option value="">(error)</option>';
    }
  }

  // Session change handler
  sessionSelect.addEventListener('change', () => {
    currentSessionKey = sessionSelect.value;
    localStorage.setItem('mewchat-session', currentSessionKey);
    // Clear reply watcher to prevent leaks
    if (chatReplyWatcher) { clearInterval(chatReplyWatcher); chatReplyWatcher = null; }
    stopSSE();
    chatMessages.innerHTML = '';
    chatData = [];
    lastMessageCount = 0;
    unreadBannerCount = 0;
    updateNewMessagesBanner();
    startSSE(currentSessionKey);
    loadDraftForCurrentSession();
  });

  // Session search/filter functionality
  const sessionSearch = document.getElementById('session-search');
  let allSessionOptions = []; // store all session {key, label} for filtering

  function cacheSessionOptions() {
    allSessionOptions = Array.from(sessionSelect.options).map(opt => ({
      value: opt.value,
      text: opt.textContent
    }));
  }

  function filterSessions(query) {
    if (allSessionOptions.length === 0) return;
    const normalizedQuery = query.toLowerCase().trim();
    sessionSelect.innerHTML = '';
    let visibleCount = 0;
    allSessionOptions.forEach(opt => {
      if (!opt.value) return;
      const matches = !normalizedQuery || 
        opt.text.toLowerCase().includes(normalizedQuery) || 
        opt.value.toLowerCase().includes(normalizedQuery);
      if (matches) {
        const option = document.createElement('option');
        option.value = opt.value;
        option.textContent = opt.text;
        sessionSelect.appendChild(option);
        visibleCount++;
      }
    });
    // Determine which session should be selected
    let newSessionKey = null;
    if (currentSessionKey && allSessionOptions.some(opt => opt.value === currentSessionKey)) {
      const stillVisible = Array.from(sessionSelect.options).some(opt => opt.value === currentSessionKey);
      if (stillVisible) {
        newSessionKey = currentSessionKey;
      } else if (sessionSelect.options.length > 0) {
        newSessionKey = sessionSelect.options[0].value;
      }
    } else if (sessionSelect.options.length > 0) {
      newSessionKey = sessionSelect.options[0].value;
    }
    
    if (newSessionKey && newSessionKey !== currentSessionKey) {
      currentSessionKey = newSessionKey;
      localStorage.setItem('mewchat-session', currentSessionKey);
      sessionSelect.value = newSessionKey;
      // Trigger session change handler to switch sessions
      sessionSelect.dispatchEvent(new Event('change'));
    } else if (newSessionKey) {
      sessionSelect.value = newSessionKey;
    }
    
    sessionSelect.disabled = visibleCount === 0;
  }

  if (sessionSearch) {
    sessionSearch.addEventListener('input', (e) => {
      filterSessions(e.target.value);
    });
  }

  // ── Enhanced sendMessage from dashboard ──────────────────────────────────
  async function sendMessage(textOverride = null) {
    const text = textOverride || msgInput.value.trim();
    if (!text || !currentSessionKey) return;

    // Clear input
    if (!textOverride) {
      msgInput.value = '';
      msgInput.style.height = 'auto';
      if (charCountEl) charCountEl.textContent = '0';
    }

    sendBtn.disabled = true;
    sendBtn.textContent = '⏳';
    chatSending = true;
    clearError();

    // Optimistic UI: add user message immediately
    const tempId = 'msg-' + Date.now();
    const div = document.createElement('div');
    div.className = 'msg user sending';
    div.id = tempId;
    div.innerHTML = `<div class="msg-bubble">${esc(text)}</div><div class="msg-meta">👤 You · sending…</div>`;
    chatMessages.appendChild(div);
    scrollChat();

    try {
      const res = await fetch(API_BASE + '/api/send', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({message: text, sessionKey: currentSessionKey})
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to send');

      const el = document.getElementById(tempId);
      if (el) {
        el.classList.remove('sending');
        el.querySelector('.msg-meta').textContent = '👤 You · ' + new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
      }

      showTypingIndicator();

      // Poll until a NEW assistant message appears
      const sentAt = Date.now();
      const asstMsgs = chatData.filter(m => m.role !== 'user');
      const lastAsstTs = asstMsgs.length ? new Date(asstMsgs[asstMsgs.length - 1].ts).getTime() : 0;

      // Clear any existing watcher
      if (chatReplyWatcher) { clearInterval(chatReplyWatcher); chatReplyWatcher = null; }

      chatReplyWatcher = setInterval(async () => {
        try {
          const r = await fetch(API_BASE + '/api/chat?sessionKey=' + encodeURIComponent(currentSessionKey));
          if (!r.ok) return;
          const d = await r.json();
          const msgs = d.chat || [];
          const newAsst = msgs.filter(m => m.role !== 'user' && new Date(m.ts).getTime() > lastAsstTs);
          const timedOut = Date.now() - sentAt > 180000; // 3 min timeout

          if (newAsst.length > 0 || timedOut) {
            clearInterval(chatReplyWatcher);
            chatReplyWatcher = null;
            chatSending = false;
            removeTypingIndicator();
            renderChat(msgs, true);
          }
        } catch {}
      }, 3000);

    } catch (e) {
      chatSending = false;
      const el = document.getElementById(tempId);
      if (el) el.querySelector('.msg-bubble').style.borderColor = 'var(--error)';
      showError('Send failed: ' + e.message + ' <button class="retry-btn">Retry</button>');
      const retryBtn = notificationEl.querySelector('.retry-btn');
      if (retryBtn) {
        retryBtn.addEventListener('click', () => {
          hideNotification();
          sendMessage(text);
        });
      }
    } finally {
      sendBtn.disabled = false;
      sendBtn.textContent = 'Send';
      if (sendBtn.textContent === '⏳') sendBtn.textContent = 'Send';
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
    let delay = Math.min(RECONNECT_BASE * Math.pow(2, reconnectAttempts), RECONNECT_MAX);
    // Add jitter (±20%) to avoid thundering herd
    const jitter = 0.8 + Math.random() * 0.4; // 0.8-1.2
    delay = Math.floor(delay * jitter);
    reconnectAttempts++;

    // Show status message in chat
    showReconnectStatus();

    reconnectTimeout = setTimeout(() => {
      console.log(`[MewChat] Reconnection attempt ${reconnectAttempts} in ${delay}ms (with jitter)`);
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
      // Show loading indicator for initial load (not for reconnects where chat already loaded)
      if (!isReconnect) {
        showLoadingChat();
      }
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
      removeLoadingChat();
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
        
        // Skip SSE updates while sending to avoid flash
        if (chatSending) return;
        
        // Use renderChat for consistent rendering with scroll preservation
        renderChat(data.chat, true);
        updateLastUpdated();
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
      case 'tab':
        e.preventDefault();
        const direction = e.shiftKey ? -1 : 1;
        const currentIdx = sessionSelect.selectedIndex;
        const optionCount = sessionSelect.options.length;
        if (optionCount <= 1) break;
        let newIdx = currentIdx + direction;
        if (newIdx >= optionCount) newIdx = 0;
        if (newIdx < 0) newIdx = optionCount - 1;
        sessionSelect.value = sessionSelect.options[newIdx].value;
        sessionSelect.dispatchEvent(new Event('change'));
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
    CHAR_LIMIT: 'mewchat-char-limit',
    SHOW_TIMESTAMPS: 'mewchat-show-timestamps',
    SHOW_MASCOT: 'mewchat-show-mascot',
    HIDE_SYSTEM_MSGS: 'mewchat-hide-system-msgs'
  };

  const DEFAULT_SETTINGS = {
    typewriterEnabled: true,
    typewriterSpeed: 25,
    mascotAnimation: true,
    charLimit: 0,
    showTimestamps: true,
    showMascot: true,
    hideSystemMsgs: false
  };

  function loadSettings() {
    const stored = {};
    for (const [key, storageKey] of Object.entries(SETTINGS_KEYS)) {
      const value = localStorage.getItem(storageKey);
      if (value !== null) {
        if (key.includes('SPEED') || key.includes('CHAR_LIMIT')) {
          stored[key] = parseInt(value, 10);
        } else if (key.includes('ENABLED') || key.includes('ANIMATION') || key.includes('SHOW_') || key.includes('HIDE_')) {
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
    const showTimestampsCheckbox = document.getElementById('setting-timestamps');
    const showMascotCheckbox = document.getElementById('setting-showmascot');
    const hideSystemMsgsCheckbox = document.getElementById('setting-hidesystem');

    if (typewriterCheckbox) typewriterCheckbox.checked = settings.typewriterEnabled;
    for (const radio of speedRadios) {
      radio.checked = parseInt(radio.value, 10) === settings.typewriterSpeed;
    }
    if (mascotCheckbox) mascotCheckbox.checked = settings.mascotAnimation;
    if (charLimitSelect) charLimitSelect.value = settings.charLimit.toString();
    if (showTimestampsCheckbox) showTimestampsCheckbox.checked = settings.showTimestamps;
    if (showMascotCheckbox) showMascotCheckbox.checked = settings.showMascot;
    if (hideSystemMsgsCheckbox) hideSystemMsgsCheckbox.checked = settings.hideSystemMsgs;
  }

  function saveSettings() {
    const typewriterEnabled = document.getElementById('setting-typewriter')?.checked ?? DEFAULT_SETTINGS.typewriterEnabled;
    const speedRadio = document.querySelector('input[name="typewriter-speed"]:checked');
    const typewriterSpeed = speedRadio ? parseInt(speedRadio.value, 10) : DEFAULT_SETTINGS.typewriterSpeed;
    const mascotAnimation = document.getElementById('setting-mascot')?.checked ?? DEFAULT_SETTINGS.mascotAnimation;
    const charLimit = parseInt(document.getElementById('setting-charlimit')?.value ?? '0', 10);
    const showTimestamps = document.getElementById('setting-timestamps')?.checked ?? DEFAULT_SETTINGS.showTimestamps;
    const showMascot = document.getElementById('setting-showmascot')?.checked ?? DEFAULT_SETTINGS.showMascot;
    const hideSystemMsgs = document.getElementById('setting-hidesystem')?.checked ?? DEFAULT_SETTINGS.hideSystemMsgs;

    localStorage.setItem(SETTINGS_KEYS.TYPEWRITER_ENABLED, typewriterEnabled);
    localStorage.setItem(SETTINGS_KEYS.TYPEWRITER_SPEED, typewriterSpeed);
    localStorage.setItem(SETTINGS_KEYS.MASCOT_ANIMATION, mascotAnimation);
    localStorage.setItem(SETTINGS_KEYS.CHAR_LIMIT, charLimit);
    localStorage.setItem(SETTINGS_KEYS.SHOW_TIMESTAMPS, showTimestamps);
    localStorage.setItem(SETTINGS_KEYS.SHOW_MASCOT, showMascot);
    localStorage.setItem(SETTINGS_KEYS.HIDE_SYSTEM_MSGS, hideSystemMsgs);
    applyTimestampVisibility();
    applyMascotVisibility();
    applySystemMessagesVisibility();
    hideSettings();
  }

  function resetSettings() {
    for (const [key, storageKey] of Object.entries(SETTINGS_KEYS)) {
      localStorage.removeItem(storageKey);
    }
    loadSettingsToModal();
    applyTimestampVisibility();
    applyMascotVisibility();
    applySystemMessagesVisibility();
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

    if (settings.charLimit > 0) {
      const percent = currentLength / settings.charLimit;
      const limitReached = currentLength >= settings.charLimit;

      // Progressive warning colors
      if (limitReached) {
        charCountEl.style.color = 'var(--red)';
        charCountEl.style.fontWeight = '700';
        if (!charLimitWarningShown) {
          charCountEl.textContent += ' (max reached)';
          charLimitWarningShown = true;
        }
      } else if (percent >= 0.9) {
        charCountEl.style.color = '#ffa500'; // orange
        charCountEl.style.fontWeight = '600';
        charLimitWarningShown = false;
      } else if (percent >= 0.8) {
        charCountEl.style.color = '#d29922'; // yellow
        charCountEl.style.fontWeight = '500';
        charLimitWarningShown = false;
      } else {
        charCountEl.style.color = '';
        charCountEl.style.fontWeight = '';
        charLimitWarningShown = false;
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
    loadDraftForCurrentSession();
    // Apply initial UI settings
    applyTimestampVisibility();
    applyMascotVisibility();
    applySystemMessagesVisibility();
    // Focus input for quick start
    if (msgInput) msgInput.focus();
  });

  // ── Refresh chat on demand ──────────────────────────────────────────────
  async function refreshChat() {
    if (chatSending || !currentSessionKey) return;
    try {
      const res = await fetch(API_BASE + '/api/chat?sessionKey=' + encodeURIComponent(currentSessionKey));
      if (!res.ok) return;
      const data = await res.json();
      renderChat(data.chat, true);
    } catch {}
  }
})();

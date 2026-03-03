# MewChat 🐾

A standalone, kawaii chat web app for talking with **mewmew** — your OpenClaw assistant.

- Uses the same theme & mascot as MewDash
- Session selector to switch between your chats/agents
- Real-time polling for new messages
- PWA: add to home screen on Android/iOS
- Light/dark theme toggle
- **Modular**: HTML, CSS, JS separated

## Quick Start

1. Ensure MewDash backend is running on `http://localhost:3001` (or adjust `config.js`).
2. Start the server:

```bash
cd /home/ubuntu/.openclaw/workspace/apps/mewchat
./run.sh
```

3. Open **http://localhost:3002** in your browser.

## File Structure

```
mewchat/
├── index.html    # Main HTML (minimal, references CSS/JS)
├── kawaii.css    # Kawaii cyberpunk theme
├── app.js        # Application logic (fetch, render, polling)
├── config.js     # API_BASE and constants
├── manifest.json # PWA manifest
├── run.sh        # Local dev server launcher
└── README.md
```

## Configuring the API

Edit `config.js` to point to your MewDash backend:

```js
const CONFIG = {
  API_BASE: 'https://your-clawdash.example.com', // change this
  POLL_INTERVAL: 3000,
  MAX_MESSAGES: 500,
};
```

## Deploy Anywhere

This is a static site. Deploy to:
- Vercel / Netlify / Cloudflare Pages
- GitHub Pages
- Any static web host

Just upload the files and set `API_BASE` appropriately. The backend must have CORS enabled (MewDash does `*` by default).

## Features

- Session list from `/api/sessions`
- Chat history from `/api/chat?sessionKey=...`
- Send via `/api/send`
- Auto-poll every 3s for new replies
- Responsive design (mobile-friendly)
- PWA manifest for "Add to Home Screen"

Enjoy your kawaii chat experience! (♡ω♡)♪
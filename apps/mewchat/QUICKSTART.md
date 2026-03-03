# Quick Start

## Option 1: Run locally (recommended for testing)

```bash
cd /home/ubuntu/.openclaw/workspace/apps/mewchat
./run.sh
```

Then open **http://localhost:3002** in your browser.

## Option 2: Deploy as static site

1. Upload the files to any static host (Vercel, Netlify, GitHub Pages, etc.)
2. Edit `config.js` and set `API_BASE` to your MewDash backend URL (e.g., `https://your-clawdash.vercel.app`)
3. Ensure that backend allows CORS from your domain (MewDash allows `*`)

That's it! Enjoy kawaii chatting! (♡ω♡)♪
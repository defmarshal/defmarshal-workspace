# Option 1: Publish Research Publicly — Progress Log

**Last updated:** 2026‑02‑22 16:00 UTC

---

## ✅ Implemented

### Research Hub (Live)
- **URL:** https://research-hub-flame.vercel.app
- **Tech:** Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS
- **Content:** 181 research reports + 181 MP3 narrations (100% TTS coverage)
- **Features:**
  - Responsive list view with search
  - Individual report pages with audio player
  - Audio badge on list when TTS available
  - Dynamic routing for `/research/[slug]`
  - RSS feed at `/feed` (for Zapier auto‑tweet)

### Auto‑Deploy Pipeline
- Script: `scripts/deploy-research-hub.sh`
  - Runs `prebuild.sh` (syncs `.md` + `.mp3` to `public/research`)
  - Deploys via `vercel --prod`
- Hooked into `agents/research-cycle.sh`: triggers when new reports are generated and narrated

### Auto‑Tweet (via Zapier)
- RSS feed endpoint: `/feed` ( route.ts )
- XML escaping for safety
- Zapier setup instructions:
  1. Trigger: RSS by Zapier → Feed URL `https://research-hub-flame.vercel.app/feed`
  2. Action: Twitter → Create Tweet (`{{Title}} — {{Link}}`)
- No Twitter API costs (free Zapier tier: 100 tasks/month, 15‑min checks)

### Newsletter (Daily Digest)
- Script: `scripts/send-research-digest.sh`
  - Sends HTML email via Maton Gmail API
  - Includes list of new reports with links and audio indicator
- Quick command: `./quick send-digest`
- Proposed cron: `research-digest-cron` (daily 18:00 ICT) – documented in `CRON_JOBS.md`

### Analytics
- GA4 placeholder in `apps/research-hub/app/layout.tsx`
- Enable by setting `NEXT_PUBLIC_GA_ID` in Vercel environment variables

---

## 🔧 Outstanding Configuration

1. **Zapier**
   - Create Zap with RSS feed URL
   - Connect Twitter account
   - Publish and test

2. **Newsletter Cron**
   - Set `DIGEST_TO_EMAIL` environment variable
   - Add cron job via `openclaw cron add` (see `CRON_JOBS.md`)

3. **Analytics**
   - Add `NEXT_PUBLIC_GA_ID` in Vercel project settings

4. **Custom Domain (optional)**
   - Add in Vercel dashboard → Domains
   - Update `NEXT_PUBLIC_SITE_URL` in Vercel env if desired

---

## 📦 Commits

- `1165e170` feat(research-hub): Add audio player, syncing for mp3 files, audio badge on list
- `32dae30b` feat: Auto-deploy Research Hub after new reports
- `d8490e51` feat: Add auto‑tweet, newsletter, and analytics to Research Hub
- `ac033bd9` feat: Add RSS feed for Zapier auto‑tweet

---

## 🚀 Next Steps

- [ ] Set up Zapier and test tweet
- [ ] Configure daily digest email recipient and enable cron
- [ ] Add GA4 measurement ID to Vercel
- [ ] (Optional) Add custom domain

---

All core functionality is implemented and deployed. Just add credentials to go fully live!

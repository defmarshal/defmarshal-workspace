# OpenClaw Privacy Policy Assessment (2026-02-15)

**Assessor:** Research-agent  
**Date:** 2026-02-15 13:54 UTC  
**Sources:**
- `setupopenclaw.com/privacy` (Cloud Setup Guide) — Last updated: January 2026
- `openclawskills.best/legal/privacy/` (Skills Directory)
- `docs.openclaw.ai/gateway/security` (Product Security Model)

---

## Executive Summary

OpenClaw’s privacy posture comprises **three distinct layers**:

1. **Website privacy policies** (setupopenclaw.com, openclawskills.best): Standard website analytics and contact forms.
2. **Product data handling** (Gateway, agents, nodes): Described in security documentation, not a traditional “privacy policy.”
3. **Operational trust model**: Your OpenClaw instance processes your data locally; cloud components (skills registry, model APIs) have their own policies.

**Bottom line:** There is no single unified “OpenClaw privacy policy.” Privacy is determined by:
- Your local configuration (who can DM the bot, what tools it can use)
- Third‑party services (LLM providers, skill APIs, cloud skills)
- The security practices you implement (allowlists, sandboxing, encryption)

---

## 1. Website Privacy Policies

### 1.1 `setupopenclaw.com` (Cloud Setup Guide)

**Collected data:**
- Analytics: page views, referral sources, country‑level location (anonymous)
- Contact info: email address + message content when you contact support
- Cookies: analytics + affiliate tracking (no advertising cross‑site)

**Third‑party services:**
- Polar.sh (payments for OpenClaw Cloud)
- Google AdSense (ads; uses cookies)
- Privacy‑focused analytics (unnamed)

**Your rights:** Request data deletion, opt out of analytics via browser extensions, manage Google ad preferences.

**Assessment:** Standard, minimal website policy. Not highly concerning.

---

### 1.2 `openclawskills.best` (Skills Directory)

**Collected data:**
- Usage data: pages visited, referrers, approximate device info
- Contact data: email + message if you contact support
- Skill metadata: public repository data (README, SKILL.md) to render listings

**Data retention:** As long as needed to provide services or comply with legal obligations.

**Assessment:** Also standard and minimal. No sensitive personal data collected intentionally.

---

## 2. Product Data Handling (Docs.openclaw.ai/security)

This is the **core of OpenClaw’s privacy posture**. The software is designed as a local‑first AI agent with extensive real‑world tool access.

### 2.1 Threat Model (explicitly stated)

> Your AI assistant can:
> - Execute arbitrary shell commands
> - Read/write files
> - Access network services
> - Send messages to anyone (if you give it WhatsApp access)
>
> People who message you can:
> - Try to trick your AI into doing bad things
> - Social engineer access to your data
> - Probe for infrastructure details

The threat is **prompt injection** leading to unauthorized actions.

### 2.2 Access Control Philosophy

**Identity first → Scope next → Model last**

1. **Who can talk to the bot?**
   - DM policy (`dmPolicy`): `pairing` (default), `allowlist`, `open`, `disabled`
   - Pairing codes (expire in 1 hour); pending requests capped at 3
   - Group allowlists (`allowFrom` per channel)
   - Mention gating (requireMention)

2. **Where can the bot act?**
   - Tool access controlled by `toolPolicy` and `tools` profiles
   - Sandboxing (Docker) for file system and network isolation
   - `elevated` flag requires explicit sudoers configuration
   - Node execution (`system.run`) requires node pairing + Mac approval UI

3. **Assume the model can be manipulated**; design so manipulation has limited blast radius.

### 2.3 Data Storage

- **Session logs:** `~/.openclaw/agents/<agentId>/sessions/*.jsonl` (plaintext on disk)
  - Required for continuity and optional memory indexing
  - **Privacy implication:** Any OS user with filesystem access can read transcripts. Lock down `~/.openclaw` perms to `700`.
  - If multiple people can DM the bot, use `session.dmScope: "per-channel-peer"` to isolate contexts.

- **Credentials:**
  - Stored in `~/.openclaw/credentials/` (per‑channel JSON files)
  - Recommended: files `600`, directory `700`
  - Examples: WhatsApp credentials, Telegram bot token, Discord bot token, Slack tokens, pairing allowlist (`-allowFrom.json`), model auth profiles

- **Memory indices:** `MEMORY.md`, `memory/` daily logs, `openclaw-memory` storage (if installed)
  - These are local files you control.

### 2.4 Network Exposure

- Gateway binds to `localhost:8080` by default.
- If you expose it (Tailscale Funnel, reverse proxy), you must:
  - Enable `gateway.auth` (password or tokens)
  - Configure `gateway.trustedProxies` to prevent IP spoofing
  - Avoid `gateway.controlUi.allowInsecureAuth` and `gateway.controlUi.dangerouslyDisableDeviceAuth` (severe downgrade)
- `openclaw security audit` checks these automatically.

### 2.5 Plugin Security

- Plugins run in‑process with the Gateway.
- Treat plugin folders as trusted code.
- `plugins.allow` allowlist recommended.
- `openclaw plugins install` runs `npm install --omit=dev` which executes lifecycle scripts → treat like running untrusted code.

---

## 3. Third‑Party Services & Data Sharing

OpenClaw itself is local, but skills and models often call external APIs:

- **LLM providers:** OpenRouter, Voyage, OpenAI, etc. → your prompts/completions sent to them.
- **Skill APIs:** Nekos (selfie), Jikan (anime), Maton (Gmail), etc. → data shared per skill scope.
- **Cloud skills:** Some skills may route through cloud services; check skill docs.
- **OpenClaw Cloud:** If you use hosted service, their terms apply.

**Mitigation:** Prefer local models where possible; review skill permissions; use API keys with limited scopes; monitor logs.

---

## 4. Privacy‑ Enhancing Configuration Recommendations

| Feature | Setting | Rationale |
|---------|---------|-----------|
| DM policy | `pairing` (default) or `allowlist` | Prevents strangers from triggering the bot |
| Group policy | `allowlist` + `requireMention: true` | Reduces accidental triggers |
| Session isolation | `session.dmScope: "per-channel-peer"` if multiple users can DM | Prevents cross‑user data leakage |
| Tool policy | Use `minimal` or custom whitelist; avoid `*` | Limits blast radius from prompt injection |
| Sandboxing | Enable `tools.sandbox` (Docker) for file/network tools | Isolates shell commands |
| Elevated commands | Only after `sudoers` NOPASSWD with explicit `elevated: true` in tool config | Prevents accidental privilege escalation |
| Permissions | `chmod 700 ~/.openclaw`; files `600` | Blocks other OS users from reading logs/credentials |
| Gateway auth | Always use `gateway.auth` (password or token) if exposing network | Prevents unauthorized control |
| Audit | Run `openclaw security audit` regularly | Catches misconfigurations |

---

## 5. Gaps & Concerns

### 5.1 No Unified Privacy Policy for the Product

- The docs explain security and access control, but not in “privacy policy” format.
- Users must piece together information from security docs, skill docs, and third‑party policies.
- **Recommendation:** Publish a clear privacy policy that covers:
  - What data the Gateway stores locally (session logs, memory, credentials)
  - When and how data is sent to third parties (LLMs, skills)
  - Retention periods and deletion procedures
  - User rights (export, delete)

### 5.2 Local Logs Retention Unclear

- Security docs say logs are kept for continuity, but no retention policy.
- Logs can grow indefinitely; no built‑in rotation mentioned.
- **Recommendation:** Implement log rotation and an easy “clear session history” command.

### 5.3 Cloud Skills & Telemetry Unknown

- The “OpenClaw Cloud” service (if used) may collect usage data; policy at `setupopenclaw.com/privacy` covers only the website and payment, not the cloud agent service itself.
- **Recommendation:** Clarify what data OpenClaw Cloud collects from running agents.

### 5.4 Third‑Party Skill Privacy

- Skills listed in the directory have no standardized privacy disclosures.
- Users must read each skill’s source or documentation to know where data goes.
- **Recommendation:** Introduce a privacy “badge” or require skills to declare data destinations (similar to OAuth scopes).

---

## 6. Comparison: Self‑Hosted vs OpenClaw Cloud

| Aspect | Self‑Hosted (local Gateway) | OpenClaw Cloud |
|--------|----------------------------|----------------|
| Data residency | Entirely on your machine | Some data may go through cloud infrastructure |
| LLM provider | Your choice (OpenRouter, local Ollama, etc.) | Likely managed by OpenClaw team |
| Updates | You control timing | Managed by provider |
| Support | Community / DIY | Included with subscription |
| Privacy responsibility | You configure access controls, encryption, auth | Provider shares responsibility; check their policy |

---

## 7. Conclusion & Action Items

**For the user (def, this workspace):**
- Current setup appears **reasonably secure**:
  - `dmPolicy: pairing` is default (we have no explicit config showing open DMs)
  - Credentials stored in `~/.openclaw/credentials/` (permissions should be `600`)
  - `sudoers` configured for elevated commands (tight control)
  - Daemons running under the same user (no separate OS users)
- Recommended improvements:
  - Verify `session.dmScope` is appropriate (currently `main` – okay if only you use DMs)
  - Run `openclaw security audit` regularly (could be added to `quick health`)
  - Consider log rotation (e.g., `logrotate` or custom script)
  - Document third‑party APIs used by installed skills (we already use Gmail, nyaa, weather, etc.)

**For OpenClaw project:**
- Publish a comprehensive privacy policy covering the Gateway software.
- Add data retention controls (auto‑expire session logs, memory pruning).
- Implement skill privacy labels.
- Consider encrypted credential storage (e.g., libsodium or OS keychain integration).

---

**Overall assessment:** The product emphasizes **security through access control** rather than formal privacy policies. The model is local‑first with explicit trust boundaries. However, the lack of a unified privacy policy makes it harder for users to understand data flows at a glance. Given the sensitive tools (email, shell, messaging), the **security model is sound** if configured properly, but **privacy transparency needs improvement**.

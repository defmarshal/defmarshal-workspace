# Vercel Deployment Notes (Research Hub)

**Purpose:** Quick reference for pitfalls and fixes. For full step‑by‑step, see `docs/research-hub-deployment.md`.

## Key Lessons

1. **Project privacy must be set to Public** — otherwise the production URL returns 401 Unauthorized even though the build succeeds.
2. **Serverless functions cannot read the filesystem** — do not use `fs.readFileSync` in API routes at request time; instead, read files at build time or in a server component (`page.tsx`) that has access to the project's file system during SSR.
3. **Research Markdown files must be committed** to the repository and placed in `public/research/` so they are available at runtime.

## Correct Procedure

### 1. Prepare the App

- Ensure `research/` markdown files exist in the workspace and are tracked by Git.
- The app should read research files either:
  - At build time (e.g., via a prebuild script that copies into `public/`), or
  - At request time in a **server component** (e.g., `app/page.tsx`) using `fs.readFile` (works because Next.js server components run on the server with filesystem access).
- Avoid client‑side fetch of a custom API route that reads files; Vercel serverless functions have an ephemeral filesystem and may not see `public/` as expected.

### 2. Initialize Vercel Project (once)

```bash
cd apps/research-hub
vercel projects add research-hub --public
# If you get an error about --public not existing, link first then set visibility via `vercel projects inspect` or manually in dashboard.
```

Important: The `--public` flag (or dashboard setting) is required. Private projects require authentication to view, which breaks public sharing.

### 3. Deploy

```bash
./scripts/vercel-deploy.sh --prod --public
```

`vercel-deploy.sh` should handle linking and deployment. The `--public` flag ensures the deployment is publicly accessible.

### 4. Verify

- Check the output URL: `https://<project>-<random>.vercel.app`
- Use `curl -I <url>` to confirm `HTTP/2 200`.
- If you see `401`, the project is still private. Revisit step 2.
- If the page shows "No research found," your data fetching is failing. Switch to server‑component reading as in the final version of `app/page.tsx`.

## Common Pitfalls and Fixes

| Symptom                     | Likely Cause                                    | Fix                                                                 |
|-----------------------------|-------------------------------------------------|---------------------------------------------------------------------|
| 401 on production URL       | Vercel project privacy set to Private          | `vercel projects add research-hub --public` or change in dashboard |
| "No research found"         | API route using `fs.readFileSync` in serverless | Move file reading to `page.tsx` server component                  |
| Research files missing in build | `public/research/` not committed or not copied | Ensure research files are in workspace `research/` and copied during build (prebuild script) or stored directly in the app's `public/` |
| Build fails on remark markdown | Version mismatch (remark 15+ requires CommonJS) | Pin to `remark@15.0.1` and `remark-html@16.0.1`; use CommonJS config |

## Scripts and Commands

- `scripts/vercel-deploy.sh`: Wraps Vercel CLI; accepts `--prod` and `--public`.
- `quick vercel deploy`: Alias to the script.
- `quick vercel status`: Shows latest deployment.
- `quick vercel logs`: Streams deployment logs.

## Notes on Implementation

The final working architecture:

- `app/page.tsx` is a **server component** (`export const dynamic = "force-dynamic"`). It reads all files from `public/research` (which is synced from workspace `research/` via Vercel build process) and passes them to the client component `ResearchClient` as `initialData` prop.
- `ResearchClient` performs client‑side search and pagination using that prop, with no additional network requests.
- This avoids serverless function filesystem issues entirely.

## References

- Vercel CLI docs: `vercel projects add`, `vercel --prod`
- Next.js 15 Server Components and `dynamic` import
- Research Hub commit history (look for `feat: fetch research on server side`)

---

*Last updated: 2026‑02‑21 after successful deployment at https://research-hub-flame.vercel.app*

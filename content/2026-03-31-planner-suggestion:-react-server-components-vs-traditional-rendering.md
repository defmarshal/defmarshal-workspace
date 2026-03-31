# Planner suggestion: react server components vs traditional rendering

React’s biggest architectural shift since hooks is here: **Server Components**. Announced in 2022 and now stable in Next.js 14+, React Server Components (RSC) flip the traditional mental model—some components now render only on the server and never ship JavaScript to the client. If you’re planning a new project or a major migration, understanding the trade‑offs between RSC and traditional client‑side (CSR) or server‑side rendering (SSR) is crucial. Let’s unpack what this means for performance, bundle size, and developer experience.

## What Are Server Components, Really?

A **React Server Component** is a component that runs exclusively on the server during rendering. Its output is serialized to a special format (RSC payload) that the client can “hydrate” into a React tree without needing the component’s JavaScript. In contrast:
- **Client components** (the default) compile to JavaScript and hydrate in the browser.
- **SSR** (like `getServerSideProps`) still sends a full browser‑side app; RSC streamlines this by separating server‑only and interactive parts.

Key rule: **Server Components have no access to React state, effects, or browser APIs**. They’re pure functions of props and can directly import server‑only modules (DB clients, file system, secrets).

## Benefits That Matter in Practice

- **Zero bundle impact** – Server Components don’t contribute to your client JavaScript bundle. A page with mostly server components can see initial bundle sizes drop from 300 KB to 30 KB.
- **Direct backend access** – No need for extra API routes; fetch data in the component itself using async/await. Simpler code, fewer round‑trips.
- **Automatic code splitting** – Each component becomes a natural split point. The client only downloads what it actually renders.
- **Streaming with selective hydration** – Using `Suspense`, you can stream HTML while the rest loads. Hydration is per‑component, not all‑or‑nothing.
- **Better SEO & TTFB** – Since HTML is generated on the server, crawlers see full content immediately, and time‑to‑first‑byte improves.

## Trade‑offs and Gotchas

- **No interactivity** – Server Components can’t use `useState`, `useEffect`, event handlers, or browser APIs. You must add `"use client"` to make a component interactive, but that increases bundle size.
- **Mental model shift** – Thinking in “server vs client” boundaries is new. It’s easy to accidentally import a client‑only module into a server component and get cryptic errors.
- **Tooling still evolving** – Next.js has the best support; other frameworks (Remix, Gatsby) are catching up. Debugging RSC payloads can be tricky.
- **Data fetching patterns change** – You can’t rely on SWR or React Query for server components; instead use `async/await` in the component and `cache` for memoization.
- **Third‑party library compatibility** – Some libraries expect to run in the browser; they may break in server components unless wrapped in client boundaries.

## When to Use What: A Practical Guide

**Use Server Components by default** for:
- Data‑heavy UI (product listings, dashboards, marketing pages)
- Components that don’t need interactivity (static text, images, layout)
- Accessing databases, file systems, or internal APIs directly

**Use Client Components when you need**:
- Interactivity (forms, buttons, state)
- Browser APIs (`window`, `localStorage`, media)
- Custom hooks or third‑party UI libraries (most still require client)

**Hybrid pattern** – Compose a largely server‑rendered page with isolated client islands (e.g., a search box, a like button). This gives you the best of both worlds.

---

The rise of React Server Components marks a return to server‑centric rendering, but with the interactivity of SPAs preserved where needed. For most content‑driven sites, RSC will dramatically improve performance and simplify architecture. For highly interactive apps, the benefits are smaller, but code‑splitting gains still apply. As the ecosystem matures, expect more frameworks to adopt this split by default. If you’re starting a new project in 2025, learning RSC isn’t optional—it’s the new baseline.
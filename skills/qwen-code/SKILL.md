# Qwen Code Skill

An OpenClaw skill that provides access to Qwen Code (Alibaba's terminal AI agent) for coding, codebase analysis, and refactoring tasks.

## Policy

**Qwen Code is the designated tool for all coding tasks.** This includes:
- Writing new code (scripts, utilities, skills)
- Refactoring existing code
- Code analysis and documentation
- Test generation
- Debugging and optimization
- Code reviews

When a coding task is identified, use `qwen-code` directly rather than attempting to write code manually. This ensures higher quality, consistency, and leverages specialized coding models.

## Description

Qwen Code is a powerful terminal-based AI agent optimized for code tasks. This skill wraps its CLI (`qwen -p`) to execute single-shot coding queries.

**Use cases:**
- Codebase analysis and documentation
- Function refactoring and optimization
- Unit test generation
- Bug fixing and debugging
- Code review and suggestions

## Configuration

No special configuration needed if Qwen Code is installed globally (`npm install -g @qwen-code/qwen-code`).

Optional: Configure model providers in `~/.qwen/settings.json` (see Qwen Code docs). The skill defaults to `openrouter/auto` if no Qwen-specific provider is set.

## Commands

- `qwen-code <prompt>` - Execute a coding request via Qwen Code
  Example: `qwen-code "Refactor the function in @src/utils.ts to use async/await"`

## Notes

- Qwen Code respects file references using `@` syntax (e.g., `@file.js`)
- The skill runs in headless mode (`-p`) for non-interactive execution
- Output is streamed back to the chat
- Supports multiple model providers (Qwen, OpenAI, Anthropic, OpenRouter) based on your `~/.qwen/settings.json`

## Installation

This skill lives in `~/.openclaw/workspace/skills/qwen-code/`. Ensure the script `qwen-code` is executable.

The OpenClaw agent can call this skill like any other tool: `qwen-code "your coding task"`.

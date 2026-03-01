# Gemini CLI Skill

An OpenClaw skill that provides access to Google's Gemini CLI for general AI tasks: research, writing, analysis, web search, file operations, and shell command execution.

## Description

Gemini CLI is a powerful terminal-based AI agent from Google with built-in tools:
- Google Search grounding for real-time info
- File system operations
- Shell command execution
- Web fetching
- MCP server integration for custom tools

This skill wraps its CLI (`gemini -p`) for non-interactive execution.

**Use cases:**
- Research and knowledge synthesis
- Writing and content creation
- Data analysis and summarization
- Web search and information retrieval
- File manipulation and documentation
- Complex multi-step tasks with built-in tools

## Configuration

Install globally: `npm install -g @google/gemini-cli`

Authentication (choose one):
1. Google OAuth (recommended): `gemini` then follow browser flow
2. API key: `export GEMINI_API_KEY=your_key` from https://aistudio.google.com/apikey

## Commands

- `gemini-cli <prompt>` - Execute a general AI request via Gemini CLI
  Example: `gemini-cli "Research the latest trends in quantum computing and summarize"`

## Notes

- Gemini CLI has 1,000 free requests/day with Google account
- Supports file references (e.g., `@file.txt`) automatically
- Built-in tools provide richer capabilities than pure chat
- Use for research, writing, analysis—**use `qwen-code` for coding tasks**

## Installation

This skill lives in `~/.openclaw/workspace/skills/gemini-cli/`. Ensure `gemini` is in PATH.

The OpenClaw agent can call this skill: `gemini-cli "your task"`.

## Policy

- **Use Gemini CLI for**: general AI tasks, research, content creation, analysis, web search, file operations
- **Use Qwen Code for**: all coding-related tasks (writing, refactoring, testing, debugging)
- Choose the right tool for the job to leverage each agent's strengths

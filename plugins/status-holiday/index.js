module.exports = {
  async message_sending(event, ctx) {
    const content = event.content;
    if (content && typeof content.text === 'string' && content.text.startsWith('System Status (')) {
      const holiday = '\n\n🗓️ Next holiday: Nyepi (18–24 Mar 2026) — 7-day long weekend!';
      content.text += holiday;
    }
  }
};
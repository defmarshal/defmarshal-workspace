// Fast Gmail fetch via Maton API
const fetch = require('node-fetch');

async function main(inputs) {
  const max = inputs.max || 10;
  const apiKey = process.env.MATON_API_KEY;
  const connId = process.env.CONNECTION_ID;

  if (!apiKey) throw new Error('MATON_API_KEY not set');
  if (!connId) throw new Error('CONNECTION_ID not set');

  // 1. List recent message IDs
  const listUrl = `https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=${max}`;
  const listRes = await fetch(listUrl, {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });
  if (!listRes.ok) {
    const txt = await listRes.text();
    throw new Error(`List messages failed: ${listRes.status} ${txt}`);
  }
  const listData = await listRes.json();
  const msgs = listData.messages || [];

  if (msgs.length === 0) return [];

  // 2. Fetch details in parallel batches (concurrency = 3 to be polite)
  const concurrency = 3;
  const results = [];

  for (let i = 0; i < msgs.length; i += concurrency) {
    const batch = msgs.slice(i, i + concurrency);
    const batchPromises = batch.map(async (m) => {
      const url = `https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/${m.id}?format=metadata&metadataHeaders=From,Subject,Date`;
      const res = await fetch(url, {
        headers: { 'Authorization': `Bearer ${apiKey}` }
      });
      if (!res.ok) {
        console.warn(`Msg ${m.id} fetch failed: ${res.status}`);
        return null;
      }
      const data = await res.json();
      const headers = data.payload.headers || [];
      const get = (name) => {
        const h = headers.find(x => x.name.toLowerCase() === name.toLowerCase());
        return h ? h.value : '';
      };
      return {
        messageId: m.id,
        from: get('From'),
        subject: get('Subject'),
        date: get('Date'),
        snippet: data.snippet || ''
      };
    });
    const batchRes = await Promise.all(batchPromises);
    results.push(...batchRes.filter(Boolean));
  }

  return results;
}

module.exports = { main };

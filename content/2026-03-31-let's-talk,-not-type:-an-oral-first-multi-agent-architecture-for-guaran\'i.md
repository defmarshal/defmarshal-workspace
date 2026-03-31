# Let's Talk, Not Type: An Oral-First Multi-Agent Architecture for Guaraní

Most AI assistants expect you to type. They’re built for literate, keyboard-wielding users. But what about communities whose primary mode of communication is oral? The Guaraní people—over 6 million speakers across Paraguay, Brazil, Argentina, and Bolivia—have a rich oral tradition, yet technology forces them to adapt to text. A new paper proposes flipping the script: an **oral-first multi-agent architecture** designed from the ground up for spoken interaction in Guaraní. It’s not just a translation of English chatbots; it’s a reimagining of how AI can serve oral cultures.

## Why Guaraní Deserves an Oral-First Approach

Guaraní is a vibrant, officially recognized language with unique characteristics:
- **High oral prevalence**: Many native speakers are not literate in Guaraní, which uses a Latin-based orthography with complex diacritics.
- **Code-switching norms**: Everyday speech mixes Guaraní with Spanish or Portuguese, creating fluid bilingual utterances that text-based systems struggle with.
- **Cultural context**: Communication relies heavily on intonation, rhythm, and shared situational awareness—things lost in text.

A text‑first AI silently excludes these users. An oral‑first design puts their natural communication mode center stage.

## The Multi-Agent Architecture: Specialists in a Conversation

The system breaks the traditional single‑model chatbot into a **team of specialized agents** that collaborate in real time during a spoken dialogue:

- **Spoken Language Understanding Agent**: Transcribes Guaraní speech (with code‑switching tolerance) and extracts meaning without requiring strict grammar.
- **Cultural Norms Agent**: Ensures responses respect Guaraní conversational protocols—avoiding interruptions, using appropriate honorifics, and maintaining the relational harmony (*ñe’ẽnga*).
- **Knowledge Agent**: Retrieves factual information from a Guaraní‑centered knowledge base (local history, agriculture, traditional medicine) rather than relying on English‑biased sources.
- **Response Formulation Agent**: Crafts natural, spoken‑style replies, possibly in mixed Guaraní‑Spanish, preserving the rhythm and poetics of oral expression.
- **Turn‑Management Agent**: Handles pauses, overlaps, and back‑channel cues (“mhm, sure”) that keep spoken conversation flowing.

These agents don’t work in a pipeline; they negotiate in real time, much like human co‑speakers.

## Key Innovations That Make It Work

- **Incremental processing**: The system doesn’t wait for a full utterance. It starts understanding and responding mid‑sentence, reducing latency and feeling more like natural conversation.
- **Diacritic‑robust ASR**: Speech recognition tuned to Guaraní phonology, tolerating the missing diacritics that often plague text input.
- **Dynamic code‑switching detection**: The model identifies language boundaries on the fly and adjusts vocabulary and grammar accordingly.
- **Cultural safety layer**: Before a response is spoken, it’s vetted for cultural appropriateness—e.g., avoiding references that might be sacred or restricted to certain genders.

## Results: More Than Just Accuracy

Pilot tests with Guaraní‑speaking communities showed:
- **Higher adoption**: Users preferred the oral system over text‑based alternatives by a 3:1 margin.
- **Better task completion**: For information‑seeking tasks (e.g., “When is the next community festival?”), success rates rose from 58% (text system) to 84% (oral‑first).
- **Cultural acceptance**: Participants noted the AI “speaks like one of us,” using appropriate greetings and respecting conversational turn‑taking.

The architecture also revealed challenges: network latency in rural areas, the need for larger spoken corpora, and the importance of local community involvement in training data collection.

---

The oral‑first multi‑agent architecture for Guaraní proves that AI doesn’t have to force everyone into the text box. By designing from the cultural and linguistic realities of an oral community, we can build systems that feel native, respectful, and actually useful. This approach should be a template for other oral traditions worldwide—from Indigenous Australian languages to West African griot storytelling cultures. The future of inclusive AI isn’t just about more languages; it’s about *different* modalities of communication. Let’s talk, not type—and let the world’s oral wisdom shape how machines listen.
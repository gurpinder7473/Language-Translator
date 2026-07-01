# Language Translator

A clean, single-page language translation tool. Type text, pick a source and target language, and get an instant translation — with swap, copy, and text-to-speech built in.
https://language-translator-tvad8ttwkrbf9qpwjqvble.streamlit.app/
## Features

- Text input with source & target language selectors (30 languages)
- One-click language swap
- Copy translated text to clipboard
- Text-to-speech playback for both source and translated text (via the browser's built-in Web Speech API)
- Character counter
- Graceful error handling with clear diagnostics if a translation request fails

## Demo

Just open `index.html` in any modern browser — no build step, no dependencies, no install required.

## How it works

This is a static, single-file HTML/CSS/JS app. Translation requests are sent client-side to two free, key-less translation endpoints, in order:

1. Google's public translation endpoint (`translate.googleapis.com`)
2. [MyMemory Translation API](https://mymemory.translated.net/) as a fallback

If both fail (e.g. you're offline, or a network/firewall is blocking the request), the app shows the exact error from each provider so you can diagnose the issue.

> **Note:** These are free, unofficial/community endpoints suitable for demos and personal projects. For production use, swap in an official API — see below.

## Upgrading to Google Cloud Translation or Microsoft Translator

The free endpoints used here have rate limits and no uptime guarantees. For production-grade reliability and quality, use:

- [Google Cloud Translation API](https://cloud.google.com/translate)
- [Microsoft Azure AI Translator](https://azure.microsoft.com/en-us/products/ai-services/ai-translator)

Both require an API key, and both **must not be called directly from client-side JavaScript** (your key would be exposed). You'll need a small backend (Node.js, Python/Flask, etc.) that:

1. Receives the text + language pair from the frontend
2. Calls the translation API server-side with your secret key
3. Returns the translated text to the frontend

Happy to help build that backend if you want to go that route — just ask.

## Tech stack

- Plain HTML, CSS, and vanilla JavaScript — no frameworks, no build tools
- Google Fonts: Fraunces, Inter, IBM Plex Mono
- Browser-native Web Speech API for text-to-speech

## Project structure

```
language-translator/
├── index.html      # Everything — markup, styles, and logic
└── README.md
```

## License

MIT — see [LICENSE](LICENSE).

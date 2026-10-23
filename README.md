
# JARVIS NEXT GENERATION

Lokaler Windows-Assistent in Python. Der Chat verwendet standardmäßig Ollama;
ein Cloud-API-Schlüssel ist für den lokalen Betrieb nicht erforderlich.

## Voraussetzungen

- Windows und Python 3.13
- [Ollama für Windows](https://ollama.com/download)

## Installation und Start

Im Repository:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
ollama pull llama3.2
python -m jarvis chat
```

Ollama muss im Hintergrund laufen. Die Standardadresse ist
`http://localhost:11434`.

## Einstellungen

Kopiere `.env.example` nach `.env`, um Host, Modell oder Provider anzupassen.
Ollama ist der Standardprovider. JARVIS sendet Chatdaten nur dann an Gemini,
wenn du `JARVIS_AI_PROVIDER=gemini` auswählst und `JARVIS_GEMINI_API_KEY`
setzt. Für den lokalen Betrieb bleibt dieses Feld leer.

```env
JARVIS_AI_PROVIDER=ollama
JARVIS_OLLAMA_HOST=http://localhost:11434
JARVIS_OLLAMA_MODEL=llama3.2
JARVIS_GEMINI_API_KEY=
```

Der interaktive Chat unterstützt `/clear`, `/history` und `/exit`.

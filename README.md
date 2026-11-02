# Shelf Search

Search a small bilingual operations library by title, topic and body. The results announce their count, preserve the active filter in the URL and expose native links for keyboard navigation.

## Run

Use Python 3.12. Run `python server.py` and open http://127.0.0.1:8000. The application runs locally. Install the test tooling with `python -m pip install -r requirements-test.txt` and `python -m playwright install chromium`, then run `python -m unittest -v`. To test an installed Google Chrome, set TEST_BROWSER_CHANNEL to chrome.

The bundled corpus is synthetic. Tokens must all occur in a document. Exact title matches outrank body matches. Accent folding and case folding do not translate terms. Only HTTP(S) links to same-origin fragment records are rendered.

## Resumen en español

Explora procedimientos en español e inglés con filtros por tema, búsqueda sin tildes y enlaces navegables con teclado.

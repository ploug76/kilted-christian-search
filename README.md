# Kilted Christian Search

A free, installable web app (PWA) for searching every Kilted Christian episode transcript, with tabs for each show (Book of Heaven, Church by the Fire, and more).

- 1,136 machine-generated transcripts (Whisper) from the Podbean audio, about 19.2 million words.
- Search runs entirely in the browser against a sharded, lazy-loaded inverted index (`idx/` for words, `bi/` for two-word phrases). Transcripts are gzip-compressed per episode (`t/`).
- Each result links to the original episode page.

Transcripts are automatic and may contain recognition errors.

"""Local text review UI. Run from this repository and open http://127.0.0.1:8766."""
import html
import json
from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from ticket_parser import parse_text

def application(environ, start_response):
    text = Path(__file__).with_name('examples').joinpath('ticket-001.txt').read_text()
    result = ''
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            length = int(environ.get('CONTENT_LENGTH') or 0)
            if length < 0 or length > 50000:
                raise ValueError('Paste at most 50 KB of ticket text')
            text = parse_qs(environ['wsgi.input'].read(length).decode('utf-8')).get('ticket', [''])[0]
            result = '<h2>Extraction and review evidence</h2><pre>' + html.escape(json.dumps(parse_text(text), indent=2)) + '</pre>'
        except (ValueError, UnicodeDecodeError) as exc:
            result = '<p>' + html.escape(str(exc)) + '</p>'
    body = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
        '<title>Concrete ticket review</title><style>body{font:16px system-ui;color:#153747;background:#f2f6f8;max-width:1000px;margin:45px auto;padding:20px}'
        'textarea{width:100%;height:245px;font:15px monospace;box-sizing:border-box;padding:16px}button{background:#006c67;color:white;border:0;padding:12px 24px;margin-top:14px;border-radius:6px}'
        'pre{white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:20px;border-radius:12px}</style>'
        '<p>PUBLIC RECONSTRUCTION · SYNTHETIC EXAMPLE</p><h1>Concrete ticket review</h1>'
        '<p>Paste one labelled delivery ticket. Missing fields, dates and units appear in the review queue. Use the command-line tool for PDF, SQL and Excel export.</p>'
        '<form method="post"><label for="ticket">Ticket text</label><textarea id="ticket" name="ticket">' + html.escape(text) +
        '</textarea><br><button>Check ticket</button></form>' + result + '</html>').encode()
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(body))), ('Cache-Control', 'no-store')])
    return [body]

if __name__ == '__main__':
    print('Open http://127.0.0.1:8766 — Ctrl+C stops the local demo')
    make_server('127.0.0.1', 8766, application).serve_forever()

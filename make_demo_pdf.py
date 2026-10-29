"""Create a small text-layer PDF from the included synthetic ticket, without extra dependencies."""
from pathlib import Path

def make_pdf(text, destination):
    lines = text.splitlines()
    escaped = [s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)') for s in lines]
    stream = ('BT /F1 12 Tf 50 780 Td 18 TL ' + ' '.join('(' + s + ') Tj T*' for s in escaped) + ' ET').encode('ascii')
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
               b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'\nendstream']
    data, offsets = b'%PDF-1.4\n', [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += str(i).encode() + b' 0 obj\n' + obj + b'\nendobj\n'
    start = len(data)
    data += b'xref\n0 6\n0000000000 65535 f \n'
    data += b''.join(f'{offset:010d} 00000 n \n'.encode() for offset in offsets[1:])
    data += b'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n' + str(start).encode() + b'\n%%EOF\n'
    Path(destination).write_bytes(data)

if __name__ == '__main__':
    make_pdf(Path('examples/ticket-001.txt').read_text(), 'examples/demo-ticket.pdf')
    print('Created examples/demo-ticket.pdf from the synthetic text fixture')

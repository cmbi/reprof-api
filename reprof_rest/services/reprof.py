import re


_RE_INTP = re.compile(r'^[0-9]+$')
_FASTA_LINE_LEN = 60


def to_fasta(id_, seq, path):
    h = open(path, 'w')
    h.write('>{}\n'.format(id_))
    for i in range(0, len(seq), _FASTA_LINE_LEN):
        f = min(i + _FASTA_LINE_LEN, len(seq))
        h.write(seq[i:f] + '\n')
    h.close()


def parse_reprof(path):
    header = None
    data = []
    for line in open(path, 'r'):
        if line.startswith('#'):
            continue

        if not header:
            header = line.split()
        else:
            row = line.split()
            d = {}
            for i in range(len(row)):
                v = row[i]
                if _RE_INTP.match(v):
                    v = int(v)

                d[header[i]] = v
            data.append(d)
    return data

import re


_RE_INTP = re.compile(r'^[0-9]+$')
_FASTA_LINE_LEN = 60


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

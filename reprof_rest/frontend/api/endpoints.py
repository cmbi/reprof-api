import os
import re
import subprocess
from hashlib import md5
from tempfile import gettempdir

from flask import Blueprint, jsonify, abort, make_response, request

from reprof_rest.services.reprof import to_fasta, parse_reprof


bp = Blueprint('reprof', __name__, url_prefix='/api')

_RE_SEQP = re.compile(r'^[A-Z]+$')


@bp.route('/reprof/', methods=['POST'])
def get_reprof():
    # TODO: Use the tmpfile module to call reprof.
    # See xssp-rest mkdssp_from_pdb for an example.
    if not request.json or 'sequence' not in request.json:
        abort(400)

    seq = request.json['sequence']
    if not _RE_SEQP.match(seq):
        abort(400)

    try:
        id_ = request.json.get('id', md5(seq).hexdigest())
        fasta_path = os.path.join(gettempdir(), '{}.fa'.format(id_))
        reprof_path = os.path.join(gettempdir(), '{}.reprof'.format(id_))
    except:
        abort(500)

    reprof = None
    try:
        to_fasta(id_, seq, fasta_path)
        if not os.path.isfile(fasta_path):
            raise RuntimeError("unable to create file: {}".format(fasta_path))

        exitcode = subprocess.call(['reprof', '-i', fasta_path, '-o',
                                    reprof_path])

        if exitcode != 0 or not os.path.isfile(reprof_path):
            raise RuntimeError("unable to create file: {}".format(reprof_path))

        reprof = parse_reprof(reprof_path)
    finally:
        for path in [fasta_path, reprof_path]:
            if os.path.isfile(path):
                os.remove(path)

        if reprof:
            return jsonify({'reprof': reprof})
        else:
            abort(500)


@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

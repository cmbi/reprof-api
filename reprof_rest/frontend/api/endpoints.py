import logging
import os
import re
import subprocess
import tempfile
import textwrap
from hashlib import md5

from flask import Blueprint, jsonify, abort, make_response, request

from reprof_rest.services.reprof import parse_reprof


bp = Blueprint('reprof', __name__, url_prefix='/api')

_log = logging.getLogger(__name__)
_RE_SEQP = re.compile(r'^[A-Z]+$')


@bp.route('/reprof/', methods=['POST'])
def get_reprof():
    if not request.json or 'sequence' not in request.json:
        abort(400)

    seq = request.json['sequence']
    if not _RE_SEQP.match(seq):
        abort(400)
    id_ = request.json.get('id', md5(seq).hexdigest())

    # Create temp file for fasta input data
    tmp_file = tempfile.NamedTemporaryFile(prefix='reprof_tmp',
                                           suffix='.fasta',
                                           delete=False)
    _log.info("Created tmp file '{}'".format(tmp_file.name))

    reprof = None
    try:
        with tmp_file as f:
            f.write('>{}\n'.format(id_))
            # The fasta format recommends that all lines be less than 80 chars.
            f.write(textwrap.fill(seq, 79))

        output_filename = os.path.join(tempfile.gettempdir(),
                                       '{}.reprof'.format(id_))
        exitcode = subprocess.call(['reprof', '-i', tmp_file.name,
                                    '-o', output_filename])
        if exitcode != 0 or not os.path.exists(output_filename):
            raise RuntimeError("Error creating '{}'".format(output_filename))
        reprof = parse_reprof(output_filename)

    finally:
        _log.debug("Deleting tmp file '{}'".format(tmp_file.name))
        for f in [tmp_file.name, output_filename]:
            if os.path.exists(f):
                os.remove(f)

    return jsonify({'reprof': reprof})


@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

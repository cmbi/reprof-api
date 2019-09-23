import os
import re
from hashlib import md5

from flask import Blueprint, Flask, jsonify, abort, make_response, request

from reprof_rest.services.reprof import toFasta, parseReprof


bp = Blueprint('reprof', __name__, url_prefix='/api')

_RE_SEQP = re.compile(r'^[A-Z]+$')


@bp.route('/reprof/', methods = ['POST'])
def get_reprof():
    # TODO: Use the subprocess and tmpfile modules to call reprof.
    # See xssp-rest mkdssp_from_pdb for an example.
    if not request.json or not 'sequence' in request.json:
        abort(400)

    seq = request.json['sequence']
    if not _RE_SEQP.match(seq):
        abort(400)

    ID = request.json.get('id', md5(seq.encode()).hexdigest())

    fastaPath = '%s.fa' % ID
    reprofPath = '%s.reprof' % ID
    toFasta(ID, seq, fastaPath)
    os.system('reprof -i %s -o %s' % (fastaPath, reprofPath))

    reprof = parseReprof(reprofPath)
    os.remove(fastaPath)
    os.remove(reprofPath)

    return jsonify({'reprof' : reprof})


@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

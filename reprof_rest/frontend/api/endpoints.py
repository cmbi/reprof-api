import os,subprocess
import re
from hashlib import md5
from tempfile import gettempdir

from flask import Blueprint, Flask, jsonify, abort, make_response, request

from reprof_rest.services.reprof import toFasta, parseReprof


bp = Blueprint('reprof', __name__, url_prefix='/api')

_RE_SEQP = re.compile(r'^[A-Z]+$')


@bp.route('/reprof/', methods = ['POST'])
def get_reprof():
  # TODO: Use the tmpfile module to call reprof.
  # See xssp-rest mkdssp_from_pdb for an example.
  if not request.json or not 'sequence' in request.json:
    abort(400)

  seq = request.json['sequence']
  if not _RE_SEQP.match(seq):
    abort(400)

  try:
    ID = request.json.get('id', md5(seq).hexdigest())
    fastaPath = os.path.join(gettempdir(), '%s.fa' % ID )
    reprofPath = os.path.join(gettempdir(), '%s.reprof' % ID )
  except:
    abort(500)

  reprof = None
  try:

    toFasta(ID, seq, fastaPath)
    if not os.path.isfile( fastaPath ):
      raise RuntimeError("unable to create file: "+fastaPath)

    exitcode=subprocess.call(['reprof','-i',fastaPath,'-o', reprofPath])

    if exitcode!=0 or not os.path.isfile( reprofPath ):
      raise RuntimeError("unable to create file: "+reprofPath)

    reprof = parseReprof(reprofPath)

  finally:

    for path in [fastaPath,reprofPath]:
      if os.path.isfile( path ):
        os.remove( path )

    if reprof:
      return jsonify({'reprof' : reprof})
    else:
      abort(500)

@bp.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

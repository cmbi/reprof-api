import json

from nose.tools import eq_, ok_

from reprof_rest.factory import create_app


class TestEndpoints(object):

    @classmethod
    def setup_class(cls):
        cls.flask_app = create_app({'TESTING': True})
        cls.app = cls.flask_app.test_client()

    def test_reprof(self):
        seq = "TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN"
        rv = self.app.post('/api/reprof/',
                           data=json.dumps({'sequence': seq}),
                           content_type='application/json')
        eq_(rv.status_code, 200)
        rv_json = json.loads(rv.data)
        ok_('reprof' in rv_json)

        # Check that the correct amino acids are returned
        for residue_data in rv_json['reprof']:
            res_num = residue_data['No']
            ok_(res_num > 0)
            ok_(res_num <= len(seq))
            eq_(residue_data['AA'], seq[res_num - 1])

import os

if os.system('which reprof')!=0:
  raise Exception('Error finding reprof')

from reprof_rest.factory import create_app

app = create_app()

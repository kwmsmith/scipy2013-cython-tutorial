import sys
import pyximport
pyximport.install(setup_args=dict(script_args=['--compiler=mingw32'] if sys.platform == 'win32' else []))

import test_cython

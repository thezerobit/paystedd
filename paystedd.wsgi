import os
import sys
activate_this = '/path/to/virtualenv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# Change working directory so relative paths (and template lookup) work again
here = os.path.dirname(__file__)
os.chdir(here)
sys.path.append(here)

import bottle

import paystedd

application = bottle.default_app()


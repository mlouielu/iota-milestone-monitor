import os
import sys

sys.path.append(os.path.dirname(__name__))

from app import create_app

app = create_app()
#app.run(debug=True, host='0.0.0.0')

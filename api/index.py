import sys
import os
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from flask_app.app import create_app
    app = create_app()
except Exception as e:
    print("BOOT ERROR:", repr(e))
    traceback.print_exc()
    raise
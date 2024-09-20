import sys
import os
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware

# Adjust the Python path to point to your FastAPI app directory
path = '/home/muzammilirfan/retail-ai/backend/app'  # Change this to your project directory
if path not in sys.path:
    sys.path.append(path)

# Import your FastAPI app
from backend.app.main import app

# Wrap the FastAPI app with WSGIMiddleware
application = WSGIMiddleware(app)

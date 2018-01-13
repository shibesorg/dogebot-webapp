"""Run script"""

from config import HOST, PORT, DEBUG, RELOADER
from bottle import run
from app import app_session

run(
    app=app_session,
    host=HOST,
    port=PORT,
    debug=DEBUG,
    reloader=RELOADER,
)

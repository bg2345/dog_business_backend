from app import app, db
from app.models import User, Event, Pet

# from the app folder, import the app instance variable

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Event': Event, 'User': User, 'Pet': Pet }

from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Role

app = create_app("default")
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_processor():
    return dict(db=db, Role=Role, User=User)

if __name__ == "__main__":
    app.run(debug=True)
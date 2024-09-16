from myflaskapp import create_app, db
from myflaskapp.models import User

app = create_app()

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
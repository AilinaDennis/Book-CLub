from app import app
from app.controllers import users, pets, forums, comments

if __name__ == "__main__":
    app.run(debug=True)



from app import app
from app.controllers import users, pets, forums

if __name__ == "__main__":
    app.run(debug=True)



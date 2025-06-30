from flask import Flask
# from flask_app import create_app

# app = create_app()
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello Soham"

if __name__ == "__main__":
    app.run()
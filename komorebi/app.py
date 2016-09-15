from flask import Flask

from komorebi.web_service.user_service import user_service

app = Flask(__name__)
app.register_blueprint(user_service)


@app.route('/')
def index():
    return 'Hello world!'


if __name__ == "__main__":
    app.run()

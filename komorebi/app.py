from flask import Flask

from komorebi.web_service.user_service import user_service

app = Flask(__name__)
app.register_blueprint(user_service)


@app.route('/')
def index():
    return 'Nobody loves me it`s true not like you do'


if __name__ == "__main__":
    app.run()

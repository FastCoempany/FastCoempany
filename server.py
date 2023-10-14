from flask import Flask
app = Flask(__name__)

@app.route('/callback')
def callback():
    return "This is the callback URL!"

if __name__ == "__main__":
    app.run(port=8000)
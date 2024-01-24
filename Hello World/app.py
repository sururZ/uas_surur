from flask import Flask
app = Flask (__name__)

@app.route("/")
def helloworld():
    return "Hello World with Flask! @krisna"
if __name__ == "main":
    app.run(port=5000, debug=True)
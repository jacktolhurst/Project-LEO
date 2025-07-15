from flask import Flask, request, redirect, render_template


app = Flask(__name__)

@app.route("/")
def HomePage():
    return render_template("home.html")

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=3000)
from flask import Flask, request, redirect, render_template
from urllib.parse import urlparse
import html
import re

app = Flask(__name__)

ALLOWED_DOMAINS = [
    "192.168.1.37:3000", 
    "127.0.0.1:3000" 
]

@app.route("/", methods=["POST", "GET"])
def HomePage():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if not isSafeURL(url):
            return "Forbidden redirect!", 403
        return redirect(url, code=302)
    return render_template("home.html")

@app.route("/success.html", methods=["POST", "GET"])
def SuccessPage():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if not isSafeURL(url):
            return "Forbidden redirect!", 403
        return redirect(url, code=302)
    
    elif request.method == "POST":
        text = santiseHTML(request.form["UniqueID"])
        print(text)
    return render_template("success.html")


def isSafeURL(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.netloc and parsed_url.netloc not in ALLOWED_DOMAINS:
            return False  
        if parsed_url.scheme and parsed_url.scheme not in ["http", "https"]:
            return False  
        if re.search(r"[^\w\-/.:]", url):  
            return False  
        
        return True 
    except Exception:
        return False

def santiseHTML(text):
    return html.escape(text)

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=3000)
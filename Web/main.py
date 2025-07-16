from flask import Flask, request, redirect, render_template
from urllib.parse import urlparse
import html
import re
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)

allowedDomains = os.getenv('ALLOWED_DOMAINS')

@app.route("/", methods=["POST", "GET"])
def HomePage():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if not IsSafeURL(url):
            return "Forbidden redirect!", 403
        return redirect(url, code=302)
    return render_template("home.html")

@app.route("/success.html", methods=["POST", "GET"])
def SuccessPage():
    text = ""
    
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if not IsSafeURL(url):
            return "Forbidden redirect!", 403
        return redirect(url, code=302)
    elif request.method == "POST":
        text = SantiseHTML(request.form["UniqueID"])
        
    return render_template("success.html", message=text)


def IsSafeURL(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.netloc and parsed_url.netloc not in allowedDomains:
            return False  
        if parsed_url.scheme and parsed_url.scheme not in ["http", "https"]:
            return False  
        if re.search(r"[^\w\-/.:]", url):  
            return False  
        
        return True 
    except Exception:
        return False

def SantiseHTML(text):
    return html.escape(text)

@app.template_filter('UnSantiseHTML')
def UnSantiseHTML(text):
    return html.unescape(text)

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=3000)
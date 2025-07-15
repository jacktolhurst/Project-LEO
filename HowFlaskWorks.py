from flask import Flask, request, redirect, render_template
from urllib.parse import urlparse
import html
import re

# * initialises flask
app = Flask(__name__)

# * a list of allowed domains, atp it is ip addresses but it can be many more, like actuall websites
ALLOWED_DOMAINS = [
    "192.168.1.37:3000", 
    "127.0.0.1:3000" 
]

# * the default route, other routes for html pages ect. This is the homepage
# * methods defines the needed methods POST and GET but there are many more
@app.route("/", methods=["POST", "GET"])
def HomePage():
    # * Checks if the method is GET  and sees if it contains a url parse
    # * This is good for if i need to redirect eventually
    if request.method == "GET" and request.args.get("url"): 
        
        # * gets the url tag and returns whatever is inside it. e.g website/url=coolweb.com returns to coolweb.com
        url = request.args.get("url", "")
        
        # * this is to check if the passed URL is safe. if coolweb.com is not part of the allowed domains list it will be perma blocked
        if not isSafeURL(url):
            return "Forbidden redirect!", 403
        
        # * returns the redirected website into the main website
        return redirect(url, code=302)
    
    # * if the method is POST
    elif request.method == "POST":
        
        # * statises html feedback so it cannot run malicious code.
        # * request.form gets the form from the webpage with the id "feedback"
        feedback = santiseHTML(request.form["feedback"])
        
        # * inserts the feedback, this is meant to run in another python file and is where all databse queries are handled
        # * dbHandler is set to None in this case so the compiler does not get mad, in reality it would be set to the python file
        dbHandler = None
        dbHandler.insertFeedback(feedback)
        
    return render_template("home.html")


# * when given a url, it checks if it is in the allowed list, a https/http call and checks non allowed characters. if anything fails False
def isSafeURL(url):
    try:
        
        # * gets the url and turns it into components. e.g https://coolweb.com turns to https, coolweb, .com
        parsed_url = urlparse(url)
        
        # * if the url is not in the allowed domains, it is not safe
        if parsed_url.netloc and parsed_url.netloc not in ALLOWED_DOMAINS:
            return False  
        
        # * if the url is not a https or http, it is not safe
        if parsed_url.scheme and parsed_url.scheme not in ["http", "https"]:
            return False  
        
        # * searches the url for any weird characters
        if re.search(r"[^\w\-/.:]", url):  
            return False  
        
        # * we made it!
        return True 
    
    # * if anythign went wrong, it is not valid
    except Exception:
        return False

# * simply sanatises the input of text so it cannot perform bad code within a text element
def santiseHTML(text):
    return html.escape(text)

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=3000)
def IsGet(request):
    if request.method == "GET" and request.args.get("url"):
        return True
    else:
        return False

def IsPost(request):
    if request.method == "POST":
        return True
    else:
        return False
def html(filename):
    try:
        with open("../HTML/" + filename, "r", encoding="utf-8") as file:
            return file.read(), "text/html"
    except FileNotFoundError:
        return {"message": filename + "could not be found."}, "application/json"

def css(filename):
    try:
        with open("../CSS/" + filename, "r", encoding="utf-8") as file:
            return file.read(), "text/css"
    except FileNotFoundError:
        return {"message": filename + "could not be found."}, "application/json"

def js(filename):
    try:
        with open("../JS/" + filename, "r", encoding="utf-8") as file:
            return file.read(), "application/javascript"
    except FileNotFoundError:
        return {"message": filename + "could not be found."}, "application/json"

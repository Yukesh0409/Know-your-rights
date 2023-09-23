from flask import Flask,render_template,url_for

app = Flask("__name__")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/readdressal")
def readdressal():
    return render_template("readdressal.html")

@app.route("/legal-rights")
def legalrights():
    return render_template("legalrights.html")

@app.route("/law-and-regulations")
def Lawandregulations():
    return render_template("Lawandregulations.html")

@app.route("/legal-aid")
def legalaid():
    return render_template("legalaid.html")

@app.route("/events")
def events():
    return render_template("events.html")

@app.route("/documents")
def documents():
    return render_template("Documents.html")




if __name__ == "__main__":
    app.run(port=8080,debug=True)
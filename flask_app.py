from flask import Flask
app=Flask("First App")

@app.route("/")
def index():
	return"YEs it is working"

if __name__=="__main__":
    app.run()



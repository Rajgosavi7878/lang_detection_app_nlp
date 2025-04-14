from flask import *
import re
from pickle import load

# restore the model and vector
with open("model_ef.pkl","rb") as f:
	model = load(f)
with open("vector_ef.pkl","rb") as f:
	cv = load(f)

# text cleaning
def clean_text(txt):
	txt = re.sub(r'<[^>]+>','',txt)
	txt = re.sub(r'http\S+|www\S+|@\S+',"",txt)
	txt = re.sub(r'\d+',"",txt)
	txt = re.sub(r'\s+',' ',txt).strip()
	return txt

app = Flask(__name__)
app.secret_key = "31380c2c44c3c916b23fc4840e2471dd"

@app.route("/",methods=["GET","POST"])
def home():
	if request.method == "POST":
		txt = request.form.get("text")
		ctxt = clean_text(txt)
		vtxt = cv.transform([ctxt])
		ans = model.predict(vtxt)

		session['text'] = txt
		session['msg'] = ans[0]
		return redirect(url_for("home"))

	else:
		text = session.pop('text', '')
		msg = session.pop('msg', '')
		return render_template("home.html",text=text,msg=msg)

if __name__ == "__main__":
	app.run(use_reloader=True,debug=True)
		
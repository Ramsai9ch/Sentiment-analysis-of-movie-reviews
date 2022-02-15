import nltk
import json
import os.path
import numpy as np
from joblib import load
from nltk.corpus import stopwords
from flask import Flask, render_template, request
from database import create_movie_db, query_all, insert_review

nltk.download("stopwords")

model = load("NLP.joblib") 
vector = load("NLP_VEC.joblib")

if not os.path.isfile("movie_reviews_db.db"):
    val = create_movie_db()
    print(val)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        feedback = "NO"
        data = request.form.to_dict()
        if "yes" in data.keys():
            feedback = "YES"
        data = data["form_data"].replace("\'", "\"")
        data = json.loads(data)
        pred = data["pred"]
        review = data["review"]
        print(review, pred, feedback)
        insert_review(review,pred, feedback)
    return render_template("home.html")


@app.route("/data")
def data():
    data_obj = query_all()
    data = [i for i in data_obj]
    return render_template("data.html", data=data)
    

@app.route("/result", methods=["POST"])
def result():
    review_user=request.form["review"]
    review=review_user.lower().split()
    engStops=set(stopwords.words("english"))
    review_processed=[word for word in review if not word in engStops]
    review_processed=' '.join(review)
    review_vectorised= vector.transform(np.array([review_processed]))
    prediction = model.predict(review_vectorised)[0]
    if prediction == 0:
        out= "NEGATIVE"
    else:
        out= "POSITIVE"
    data = {}
    data["pred"] = out
    data["review"] = review_user
    # insert_review(review_user,out)
    return render_template("output.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
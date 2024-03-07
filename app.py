from flask import Flask
from flask import render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open("popular.pkl","rb"))
pt = pickle.load(open("pt.pkl","rb"))
books_df = pickle.load(open("books_df.pkl","rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl","rb"))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",
                            book_name = list(popular_df["Book-Title"].values),
                            author = list(popular_df["Book-Author"].values),
                            image = list(popular_df["Image-URL-M"].values),
                            votes = list(popular_df["num_rating"].values),
                            rating = list(popular_df["avg_rating"].values),
                            )

@app.route("/recommend")
def recommend_ui():
    
    return render_template("recommend.html")

@app.route("/recommend_books", methods=['GET', 'POST'])
def recommend():
    user_input = request.form.get("search")
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), reverse = True,key = lambda x:x[1])[:6]
    data = []
    for item in similar_items:
        temp_df = books_df[books_df["Book-Title"]==pt.index[item[0]]]
        data.extend(temp_df.drop_duplicates("Book-Title")[["Book-Title","Book-Author","Image-URL-M"]].values.tolist())
    print(data)

    return render_template("recommend.html",data = data)


if __name__ == "__main__":
    app.run(debug=True)
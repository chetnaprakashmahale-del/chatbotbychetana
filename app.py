from flask import *
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Excel file
data = pd.read_excel("convo.xlsx")

# Convert columns to lowercase (important for matching)
data["user_input"] = data["user_input"].str.lower()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    chat = ""

    if request.method == "POST":
        old_chat = request.form.get("chat", "")
        qts = request.form.get("qts", "")
        qts = qts.strip().lower()

        # Prepare text data
        texts = [qts] + data["user_input"].tolist()

        cv = CountVectorizer()
        vector = cv.fit_transform(texts)
        cs = cosine_similarity(vector)

        score = cs[0][1:]
        data["score"] = score * 100

        result = data.sort_values(by="score", ascending=False)
        result = result[result.score > 10]

        if len(result) == 0:
            msg = "Chitty ---> Sorry, I don't know the answer."
        else:
            ans = result.head(1)["bot_response"].values[0]
            msg = "Chitty ---> " + ans

        new_chat = "You said --> " + qts + "\n" + msg
        chat = old_chat + "\n" + new_chat

        return render_template("home.html", msg=msg, chat=chat.strip())

    else:
        return render_template("home.html", msg="", chat="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
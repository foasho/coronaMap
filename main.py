from flask import *
from scraping_corona import get_colona_data#追加
import os#追加

app = Flask(__name__)
#server_mode = "local"
server_mode = "heroku"

@app.route("/", methods=["GET", "POST"])
def corona_page():
    japan_corona_data = get_colona_data()#追加
    return render_template("map.html", japan_corona_data=japan_corona_data)

if __name__ == "__main__":
    if server_mode == "local":
        port = 5000
        app.run(debug=True, port=port)

    elif server_mode == "heroku":
        port = int(os.getenv("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
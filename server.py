import pickle, base64
from matplotlib.figure import Figure
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, send_file

from search import search_all_files, SearchOptions
from process_data import get_normalized_freq_over_time


options = SearchOptions(
        insert_space = True, 
        only_primary_version = False
)
INTERVAL_LEN = 50


app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
def main():
    if request.method == "POST":
        fig = Figure()
        ax = fig.subplots()
        matches = dict()
        for query, val in request.form.items():
            print(query,val)
            if val:
                curr_matches = search_all_files(val, search_options = options)
                data = get_normalized_freq_over_time(curr_matches, INTERVAL_LEN)
                X = data.keys()
                Y = data.values()
                ax.plot(X, Y, label = val)
                pickle.dump(matches, open(f"./out/{query}.pkl", 'wb'))
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        return send_file(buf, "plt.png")
    else:
        return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=50)

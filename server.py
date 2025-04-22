import pickle, base64
from matplotlib.figure import Figure
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, send_file

from defs import choosable_tags
from search import search_all_files, SearchOptions
from process_data import get_normalized_freq_over_time


INTERVAL_LEN = 50


app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def main():
	if request.method == "POST":
		print(request.form)
		all_matches = []
		options = SearchOptions(
			insert_space = True, 
			only_primary_version = False,
			text_tags = None if request.form["tag"] == 'All tags' else { request.form['tag'] }
		)
		matches = {}
		for query in ["query1", "query2", "query3", "query4", "query5"]:
			search_term = request.form[query]
			if search_term:
				curr_matches = search_all_files(search_term, search_options=options)
				matches[query] = curr_matches
		
		if "raw_matches" in request.form:
			# return the raw matches 
			table_rows = "\n".join([ match.to_html_row()
				for match in sorted(sum(matches.values(), []) , key = lambda m: m.text.date) 
			])
			html_text = f"""
			<html>
			<table>
			<tr>
				<th>Text</th>
				<th>Matching Text</th>
			</tr>
			{table_rows[:5000]}
			</table>
			</html>
			"""
			return html_text
		elif "plot" in request.form:
			# plot frequencies
			fig = Figure()
			ax = fig.subplots()
			for search_term, curr_matches in matches.items():
				data = get_normalized_freq_over_time(curr_matches, INTERVAL_LEN)
				X = data.keys()
				Y = data.values()
				ax.plot(X, Y, label = search_term)
			ax.legend()
			buf = BytesIO()
			fig.savefig(buf, format="png")
			buf.seek(0)		
			return send_file(buf, "plt.png")
		else:
			raise ValueError("something went wrong!")
	return render_template("test.html", tags = ["All tags"] + choosable_tags)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5011)

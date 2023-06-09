import matplotlib.pyplot as plt
import pickle
from search import search_all_files
from process_data import get_normalized_freq_over_time

INTERVAL_LEN = 50

for _ in range(1):
    query = [input(">").strip()]
    print(f"query: {query}")
    matches = search_all_files(query)
    print(f"{len(matches)} matches")

    data = get_normalized_freq_over_time(matches, INTERVAL_LEN)
    print(data)
    X = data.keys(); Y = data.values()

    plt.plot(X, Y, label = query[0])

plt.legend()

plt.savefig("plt.png")

from typing import *
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

from defs import Text, Match, all_texts


def get_normalized_freq_over_time(
	matches: List[Match],
	interval_len: int # 
):
	min_year = min([m.text.date for m in matches])
	min_year -= (min_year % interval_len)
	max_year = max([m.text.date for m in matches])
	max_year += (max_year % interval_len)
	matches_counts, total_counts = defaultdict(int), defaultdict(int)
	for m in matches:
		matches_counts[m.text.date - (m.text.date % interval_len)] += 1
	for text in all_texts:
		total_counts[text.date - (text.date % interval_len)] += text.word_count
	return {yr: 0 if total_counts[yr] == 0 else matches_counts[yr] / total_counts[yr] 
		for yr in range(min_year, max_year+interval_len, interval_len)}



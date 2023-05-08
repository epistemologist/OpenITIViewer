from typing import *
from collections import defaultdict, Counter
import numpy as np

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

def get_words_used_after(
    matches: List[Match],
    num_words = 3
) -> Counter:
    return Counter([tuple(m.preview_after.split()[:num_words]) for m in matches])

def get_tag_distribution(
    matches: List[Match]
):
    all_texts = {m.text for m in matches}
    all_tags = set().union(*[t.tags for t in all_texts])
    tag_dist = {tag: sum([tag in text.tags for text in all_texts]) for tag in all_tags}
    return sorted(list(tag_dist.items()), key = lambda i: i[1], reverse = True)

import pickle
matches = pickle.load(open("matches.pkl", 'rb'))


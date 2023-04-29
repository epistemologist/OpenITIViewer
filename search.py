import re, pickle
from dataclasses import dataclass
from typing import *
from concurrent.futures import ProcessPoolExecutor
from glob import glob
from tqdm import tqdm

from defs import Text, Match, all_texts, texts_by_filename


def search_file(query, filename, chars_before=None, chars_after=None) -> List[Match]:
	if chars_before is None or chars_after is None:
		chars_before = chars_after = max(100, len("".join(query))//3)
	search_regex = query.replace(" ", "[ ]*")
	doc_text = open(filename, 'r').read()
	matches = []
	for res in re.finditer(search_regex, doc_text):
		matches.append(Match(
			matched_text = doc_text[res.start(): res.end()],
			match_loc = (res.start(), res.end()),
			preview_before = doc_text[res.start()-chars_before:res.start()],
			preview_after = doc_text[res.end():res.end()+chars_after],
			text = texts_by_filename[filename.split("/")[-1].removesuffix(".raw")]
		))
	return matches

# Worker function for search_all_files to allow multithreading
def _worker(args):
#	print(args)
	return search_file(
		query = args["query"],
		filename = args["filename"],
		chars_before = args["chars_before"],
		chars_after = args["chars_after"]
	)

def search_all_files(query, chars_before=None, chars_after=None) -> List[Match]:
	all_matches = []
	def _construct_args(filename):
		return {
			"query": query,
			"filename": filename,
			"chars_before": chars_before,
			"chars_after": chars_after
		}
	with ProcessPoolExecutor(max_workers=8) as executor:
		for matches in executor.map(_worker, tqdm([_construct_args(filename) for filename in glob("./openiti_raw/*") ])):
			all_matches.extend(matches)
	return all_matches

#!/usr/bin/env python

import re
import concurrent.futures
from multiprocessing import cpu_count
from glob import glob

from util import transliterate_arabic

END_OF_META_HEADER = "#META#Header#End#\n"
EDITORIAL_CONTENT_REGEX = re.compile("^### .*?$")
ARABIC_TOKEN_REGEX = "[\u0621-\u064A\u0660-\u06690-9]+"


TOTAL_FILES = 0

def get_tokens(file, verbose=False):
	progress_bar = tqdm if verbose else (lambda x: x)
	while True:
		curr_line = file.readline()
		if curr_line == END_OF_META_HEADER:
			break

	book_text = file.read()

	def remove_extra_symbols(line):
		line = line.replace("\n~~", "")  # Remove paragraph continuation markers
		line = re.sub("PageV\d\dP\d\d\d", "", line)  # Remove page markers
		line = re.sub("ms\d\d\d\d\d", "", line)  # Remove milestone markers
		return line.strip()
	
	def paragraph_iterator(book_text):
		curr_par = ""
		for line in progress_bar(book_text.splitlines()):
			if re.match(EDITORIAL_CONTENT_REGEX, line):
				continue
			if re.match(PARAGRAPH_START, line):
				if curr_par.strip():
					yield process_paragraph(curr_par)
				curr_par = ""
			curr_par += line + "\n"
		if curr_par:
			yield process_paragraph(curr_par)

	tokens = [] 
	for line in book_text.splitlines():
		if not re.match(EDITORIAL_CONTENT_REGEX, line):
			tokens.extend([transliterate_arabic(i) for i in re.findall(ARABIC_TOKEN_REGEX, remove_extra_symbols(line))])
	return " ".join(tokens)

def parse_file(filename):
	global TOTAL_FILES
	print(filename, TOTAL_FILES)
	raw_text = get_tokens(open(filename, 'r'), verbose=False)
	f = open(f"openiti_raw/{filename.split('/')[-1]}.raw", "w")
	f.write(raw_text)
	f.close()
	TOTAL_FILES += 1

with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
	executor.map(parse_file, glob("openiti_md_files/*"))

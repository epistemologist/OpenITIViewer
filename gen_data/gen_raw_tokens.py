#!/usr/bin/env python

import re
import concurrent.futures
from multiprocessing import cpu_counbt
from glob import glob

END_OF_META_HEADER = "#META#Header#End#\n"

PARAGRAPH_START = re.compile("^#[^#].*?$")
EDITORIAL_CONTENT = re.compile("^### .*?$")

TOTAL_FILES = 0

def get_book_text(file, verbose=False):
	progress_bar = tqdm if verbose else (lambda x: x)
	while True:
		curr_line = file.readline()
		if curr_line == END_OF_META_HEADER:
			break

	book_text = file.read()

	def process_paragraph(par):
		par = par.replace("\n~~", "")  # Remove paragraph continuation markers
		par = re.sub("PageV\d\dP\d\d\d", "", par)  # Remove page markers
		par = re.sub("ms\d\d\d\d\d", "", par)  # Remove milestone markers
		return par.strip()

	def paragraph_iterator(book_text):
		curr_par = ""
		for line in progress_bar(book_text.splitlines()):
			if re.match(EDITORIAL_CONTENT, line):
				continue
			if re.match(PARAGRAPH_START, line):
				if curr_par.strip():
					yield process_paragraph(curr_par)
				curr_par = ""
			curr_par += line + "\n"
		if curr_par:
			yield process_paragraph(curr_par)

	raw_text = "\n\n\n\n".join(paragraph_iterator(book_text))
	return raw_text

def get_tokens(text):
	return " ".join(re.findall("[\u0621-\u064A\u0660-\u06690-9]+", text))

def parse_file(filename):
	global TOTAL_FILES
	print(filename, TOTAL_FILES)
	raw_text = get_tokens(get_book_text(open(filename, 'r'), verbose=False))
	f = open(f"openiti_raw/{filename.split('/')[-1]}.raw", "w")
	f.write(raw_text)
	f.close()
	TOTAL_FILES += 1


with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
	executor.map(parse_file, glob("openiti_md_files/*"))

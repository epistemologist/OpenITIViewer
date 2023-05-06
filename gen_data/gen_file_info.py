#!/usr/bin/env python

from dataclasses import dataclass
from typing import *
from tqdm import tqdm
from glob import glob
import pickle, re, csv, os
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

metadata = dict()

PATH = "openiti_data/metadata/OpenITI_metadata_2022-2-7_merged.csv"

with open(f"./{PATH}", "r") as metadata_file:
	metadata_raw = list(csv.reader(metadata_file, delimiter = '\t'))
	fields, metadata_raw = metadata_raw[0], metadata_raw[1:]
	for tmp in metadata_raw:
		filename = tmp[0]
		metadata[filename] = dict(zip(fields[1:], tmp[1:]))

texts = []

def get_word_count(filename):
	raw_text = open(f"./openiti_raw/{filename}.raw", "r").read()
	return len(raw_text.split())

def get_text_info(item):
	idx, path = item
	print(idx)
	filename = path.split("/")[-1]
	file_handle = open(path, "r")
	try:
		file_metadata = metadata[filename]
	except:
		modified_filename = ".".join(filename.split('.')[:-1])
		file_metadata = metadata[[i for i in metadata if i.startswith(modified_filename)][0]]
	# Return dict to allow for pickling
	return {
		"idx": idx,
		"filename": filename,
		"author": file_metadata["author_lat_full_name"],
		"title": file_metadata["title_lat"],
		"date": int(file_metadata["date"]),
		"tags": [i.strip() for i in file_metadata["tags"].split("::")],
		"word_count": get_word_count(filename)
	}

with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
	texts = executor.map(get_text_info, 
		tqdm(enumerate(sorted([
			f for f in glob("./openiti_md_files/*") if os.path.isfile(f)
		]))))
	texts = sorted(texts, key = lambda text: text["idx"])

pickle.dump(texts, open("texts_info.pkl", "wb"))

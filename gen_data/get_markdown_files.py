from pathlib import Path
from tqdm import tqdm
import re, os

PATH = "./openiti_data/OpenITI-data_2022-1-6"

os.system("mkdir ./openiti_md_files")

md_files = []
non_md_files = []

for path in tqdm(Path(PATH).rglob('*')):
	if path.is_file():
		f = open(path, 'r')
		first_line = f.readline()
		if re.match(f".*?OpenITI.*?", first_line):
			os.system(f"cp ./{path} ./openiti_md_files")


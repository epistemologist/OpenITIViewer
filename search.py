import re, pickle
from dataclasses import dataclass
from typing import *
from concurrent.futures import ProcessPoolExecutor
from glob import glob
from tqdm import tqdm
from multiprocessing import cpu_count

from defs import Text, Match, all_texts, texts_by_filename

@dataclass
class SearchOptions:
    insert_space: bool
    #TODO: Add more features here? (e.g. pronoun suffixes, verb conjugation, etc) 

    def gen_regex(self, queries: List[str]) -> str:
        SPACE_REGEX = "[ ]" if self.insert_space else "[ ]?"
        query_regexes = []
        for query in queries:
            query_regexes.append(query.replace(" ", SPACE_REGEX))
        return "|".join([f"({SPACE_REGEX}{i}{SPACE_REGEX})" for i in query_regexes])

def search_file(
        query: List[str], 
        filename: str, 
        search_options: SearchOptions, 
        chars_before=None, 
        chars_after=None) -> List[Match]:
    if chars_before is None or chars_after is None:
        chars_before = chars_after = max(100, len("".join(query))//3)
    search_regex = search_options.gen_regex(query)
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
#    print(args)
    return search_file(
        query = args["query"],
        search_options = args["search_options"],
        filename = args["filename"],
        chars_before = args["chars_before"],
        chars_after = args["chars_after"]
    )

def search_all_files(
    query, 
    search_options = SearchOptions(True), 
    chars_before=None, 
    chars_after=None,
    verbose=True
    ) -> List[Match]:
    all_matches = []
    def _construct_args(filename):
        return {
            "query": query,
            "search_options": search_options,
            "filename": filename,
            "chars_before": chars_before,
            "chars_after": chars_after
        }
    if verbose:
        pbar = tqdm(total=len(glob("./openiti_raw/*")))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        for matches in executor.map(_worker, [_construct_args(filename) for filename in glob("./openiti_raw/*") ]):
            all_matches.extend(matches)
            if verbose:
                pbar.update(1)
    return all_matches

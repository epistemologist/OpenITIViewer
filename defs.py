from dataclasses import dataclass
from typing import *
from multiprocessing import cpu_count
import pickle

@dataclass
class Text:
    idx: int
    filename: str
    author: str
    title: str
    date: int
    tags: List[str]
    word_count: int

@dataclass
class Match:
    matched_text: str
    match_loc: Tuple[int, int]
    preview_before: str
    preview_after: str
    text: Text

    def __repr__(self): 
        return f"{self.preview_before} **{self.matched_text}** {self.preview_after}"

all_texts = [Text(**t) for t in pickle.load(open("./texts_info.pkl", 'rb'))]
texts_by_filename = {text.filename: text for text in all_texts} 

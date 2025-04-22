# NGram browser for OpenITI Corpus

The beginnings of an n-gram viewer for the [OpenITI corpus](https://zenodo.org/record/7687795)

## Current Status
At present, the viewer only works if you have a copy of the corpus locally (which is around 33 GB); we detail how to get it below:

## Download Data

```sh
(venv) ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_data/openiti_data$ zenodo_get 10.5281/zenodo.7687795
[[ ... ]]
(venv) ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_data/openiti_data$ cat md5sums.txt 
9ff72190f7a94878834c131326d4f0b4  data.zip
39376415fea35e52cabd9292a202fcee  metadata.zip
02df73ee30a631da57c6d3d08fa9c9c7  release_notes.zip
(venv) ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_data/openiti_data$ md5sum *.zip
9ff72190f7a94878834c131326d4f0b4  data.zip
39376415fea35e52cabd9292a202fcee  metadata.zip
02df73ee30a631da57c6d3d08fa9c9c7  release_notes.zip
(venv) ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_data/openiti_data$ find *.zip | xargs -I {} unzip {}
(venv) ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_data/openiti_data/RELEASE/data$ find | wc -l
56097
```

## Get Markdown Files
```
(venv) ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_data$ time ./get_markdown_files.py 
56096it [03:18, 283.12it/s] 

real    3m18.231s
user    0m25.471s
sys     0m36.555s
```

## Patch some of the headers
```
$ diff openiti_data/RELEASE/data/1400IbnSuda/1400IbnSuda.IthafMatalic/1400IbnSuda.IthafMatalic.Sham30K0046642-ara1.completed openiti_md_files/1400IbnSuda.IthafMatalic.Sham30K0046642-ara1.completed 
71c71
< #META#Header#End
---
> #META#Header#End#
18109c18109
< ~~نقول وكيل. PageV02P0642
\ No newline at end of file
---
> ~~نقول وكيل. PageV02P0642
ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_d
```


## Generate Raw Files
```
$ time ./gen_raw_tokens.py
real    16m9.978s
user    28m51.892s
sys     2m53.632s
(venv) ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_data/openiti_raw$ find . | wc -l
11301
(venv) ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_data/openiti_raw$ du -sh .
20G     .
```

## Generate File Metadata Information
```
(venv) ubuntu@ip-172-31-28-130:~/OpenITIViewer/gen_data$ time ./gen_file_info.py
[[ ... ]] 
real    3m8.464s
user    4m11.552s
sys     1m51.397s
```

Now you should be able to run `python3 server.py` and the following webpage should come up:
![image](https://github.com/user-attachments/assets/2ef059fe-3a52-4c0f-8ff7-3c5cf0410e71)

We can plot the frequency of various terms, e.g. the Arabic word for the emperor Heraclius:
![image](https://github.com/user-attachments/assets/fa072522-0e6e-41f1-8d1d-bfb8d55287cd)


## TODO
 - clean corpus?
 - add plotting by tag
 - search method right now is messy, add different ways of searching
 	- exact match
	- match with spaces
	- levenstein distance for fuzzy matches?

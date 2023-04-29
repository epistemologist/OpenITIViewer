# NGram browser for OpenITI Corpus

The beginnings of an n-gram viewer for the [OpenITI corpus](https://zenodo.org/record/7687795)

## Build Instructions (TODO: Automate this)

**NOTE**: This takes up around 41 gigabytes of space! Keep this in mind.

### Download corpus
We can download the corpus with the `zenodo-get` library:

```sh
epistemologist@DESKTOP-MQI56O4:~/openiti$ zenodo_get 10.5281/zenodo.3082463
Title: OpenITI: a Machine-Readable Corpus of Islamicate Texts
Keywords: Arabic; Classical Arabic; Corpus
Publication date: 2022-07-08
DOI: 10.5281/zenodo.6808108
Total size: 5421.5 MB

Link: https://zenodo.org/api/files/20cd5499-2b97-4c26-8332-b1b7e6b5398b/data.zip   size: 5418.9 MB
100% [....................................................................] 5682081736 / 5682081736
Checksum is correct. (4fb22a30807a301564c76ea6a0a7d883)

Link: https://zenodo.org/api/files/20cd5499-2b97-4c26-8332-b1b7e6b5398b/metadata.zip   size: 2.5 MB
100% [..........................................................................] 2633542 / 2633542
Checksum is correct. (54090d3fbc3a730cfe5480146f122f5d)

Link: https://zenodo.org/api/files/20cd5499-2b97-4c26-8332-b1b7e6b5398b/release_notes.zip   size: 0.1 MB
100% [............................................................................] 107070 / 107070
Checksum is correct. (beb03ef40b6864ab9b2507f2a13942b5)
All files have been downloaded.
```

### Get raw Arabic files
Note that in the corpus we download, there are a mix of markdown files, the actual files of the various Arabic books, and various other files. To filter out just the raw Arabic documents, we use the `get_markdown_files.py` script to copy these files to `./openiti_md_files`

### Cleaning up corpus

Note that one of the markdown files does not contain a proper header, so we add it
```sh
$ grep -RL "#META#Header#End#"
0460ShaykhTusi.Rijal.Shia002935-ara1.mARkdown
$ diff 0460ShaykhTusi.Rijal.Shia002935-ara1.mARkdown.old openiti_md_files/0460ShaykhTusi.Rijal.Shia002935-ara1.mARkdown
37c37
< 
---
> #META#Header#End#
13283c13283
< PageV00P452
\ No newline at end of file
---
> PageV00P452
```

### Tokenize Documents
Next, to get only the raw tokens from each of the markdown files, run `./gen_raw_tokens.py`, which will generate corresponding `.raw` files in the `openiti_raw` directory (took about 6 minutes on a machine with 8 cores)

### Generating File Metadata
With the raw texts generated, we can now generate metadata about the various texts that we want to search through by running `./gen_file_info.py` (around 1 minute to run)


Now, with all of the raw files generated, you should now be able to generate plots with the `tmp_plot.py` script.


## TODO
 - clean corpus?
 - add plotting by tag
 - make a web interface


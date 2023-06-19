#!/bin/sh

set -ex

regex='([ ]HdvnA[ ])'
result=$(LC_ALL=C; grep -R -o -E --byte-offset "${regex}" ./openiti_raw | tqdm | wc -l)

echo $result

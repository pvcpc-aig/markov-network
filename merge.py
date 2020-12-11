"""
Merges the separate articleN.csv files into a single CSV file with
only a single cell per row with the cell containing the content of
the article.
"""
import os
import re
import sys

import udax.csv as csv

# All The News dataset location
DATASET = "data/allthenews"

# Name of the output file.
OUT_FILE = "articles.csv"

# An 8MB read buffer.
READ_BUFFER = 2 ** 23

# An 8MB write buffer.
WRITE_BUFFER = 2 ** 23


if __name__ == "__main__":
    if os.path.exists(f"{DATASET}/{OUT_FILE}"):
        sys.stderr.write(f"Merged datafile {OUT_FILE} exists; delete to confirm re-run.\n")
        sys.exit(1)

    parts = []
    for item in os.listdir(f"{DATASET}"):
        pattern = re.compile(r"(?:articles)[0-9]+(?:\.csv)")
        if pattern.match(item):
            parts.append(item)
    
    with open(f"{DATASET}/{OUT_FILE}", mode="w", buffering=WRITE_BUFFER) as fout:
        for part in parts:
            with open(f"{DATASET}/{part}", mode="r", buffering=READ_BUFFER) as fin:
                fin.readline() # read past the csv header
                for line in fin:
                    row = csv.parse(line)
                    if len(row) == 0:
                        continue
                    content = row[-1]
                    fout.write(f"{content}\n")
                print(f"Merged {part}...")
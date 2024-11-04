# https://gist.github.com/catawbasam/c52dbc22edb9e9c624b2cac9099f812c

import json

import pandas as pd

files = ["books/books.ndjson", "books/book_details.ndjson"]


def read(file):
    with open(file, encoding="utf-8") as f:
        lines = f.readlines()
        json_array = []
        for line in lines:
            json_array.append(json.loads(line))

        return pd.DataFrame(json_array)


df_books = read(files[0])
df_book_details = read(files[1])

df_books.to_csv("output/df_books.csv", index=False)
df_book_details.to_csv("output/df_book_details.csv", index=False)
df_books.merge(df_book_details, on="isbn").to_csv("output/final.csv", index=False)

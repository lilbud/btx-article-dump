import json
import re
from pathlib import Path

import ftfy
import html2text
import httpx
import pandas as pd
from bs4 import BeautifulSoup as bs4
from dateparser import parse
from slugify import slugify
from thefuzz import process

base_folder = Path(Path(__file__).parent, "articles")
splitpath = Path(base_folder, "split_unwrapped")


def format_md(file: Path, h: html2text.HTML2Text) -> str:
    f = Path.open(file, encoding="utf-8")
    return h.handle(ftfy.fix_text("\n".join([line.strip() for line in f.readlines()])))


def html_to_md():
    page = Path(
        r"C:\Users\bvw20\Documents\Personal\Projects\Bruce Stuff\Websites\BTX\Articles Thread",
    )

    h = html2text.HTML2Text()
    save = Path(Path(__file__).parent, "articles")

    for file in page.iterdir():
        if file.suffix == ".htm":
            formatted = format_md(file, h)

            with Path.open(Path(save, f"{file.stem}.md"), "w", encoding="utf-8") as f:
                f.write(formatted)


def unwrap_articles():
    for folder in splitpath.iterdir():
        print(folder.name)

        save_path = Path(base_folder, "split_unwrapped", folder.name)
        Path.mkdir(save_path)

        for file in folder.iterdir():
            print("\t", file.name)
            new_contents = []

            filesave = Path(save_path, file.name)

            if file.suffix == ".md":
                try:
                    with Path.open(file, "r", encoding="utf-8") as f:
                        contents = ftfy.fix_text("".join(f.readlines()))
                except (UnicodeEncodeError, UnicodeDecodeError):
                    with Path.open(file, "r", encoding="cp1252") as f:
                        contents = ftfy.fix_text("".join(f.readlines()))

                for i in contents.split("\n\n"):
                    # first pass is to catch stray new lines and
                    # double spaces and replace with single space
                    first = re.sub(r"(\n|\s{2})", " ", i)

                    # second pass is to ensure the format of the header remains
                    # otherwise, it'll wrap to a single line
                    second = re.sub(r"((Author|Source|Date)\:)", r"\n\1", first)

                    third = re.sub(r"\s$", "", second)

                    new_contents.append(third)

                try:
                    with Path.open(filesave, "w", encoding="utf-8") as f1:
                        f1.write(ftfy.fix_text("\n\n".join(new_contents).strip()))
                except UnicodeEncodeError:
                    with Path.open(filesave, "w") as f1:
                        f1.write(ftfy.fix_text(contents.strip()))


def print_article_info():
    articles = []

    for folder in splitpath.iterdir():
        # print(folder.name)
        for file in folder.iterdir():
            if file.suffix == ".md":
                try:
                    with Path.open(file, "r", encoding="utf-8") as f:
                        contents = "".join(f.readlines())
                except (UnicodeEncodeError, UnicodeDecodeError):
                    with Path.open(file, "r", encoding="cp1252") as f:
                        contents = "".join(f.readlines())

                title = re.search(r"title\: (.*)", contents)
                author = re.search(r"author\: (.*)", contents)
                source = re.search(r"source\: (.*)", contents)
                date = re.search(r"date\: (.*)", contents)
                category = re.search(r"category\: (.*)", contents)

                current = [category[1], date[1], source[1], author[1], title[1]]

                current = [i.strip('"') for i in current]
                articles.append(current)

    df = pd.DataFrame(articles)
    df.columns = ["category", "date", "source", "author", "title"]

    pd.set_option("display.max_rows", None)

    # print(df.title.groupby(df.author.str.title()).sum().reset_index())

    # for idx, name in enumerate(df["title"].value_counts().index.tolist()):
    #     if df["title"].value_counts()[idx] > 1:
    #         if len(set(df.loc[df.title == name].author.values)) > 1:
    #             print("Name :", name)
    #             print("Counts :", df["title"].value_counts()[idx])

    #             print()

    # for i in df.itertuples():
    #     if i.category == "Album Review":
    #         print(f"{i.title}, {i.author}")

    # df.to_csv("article_list.csv")
    df1 = df.groupby(["title", "author"])

    for i in df1.value_counts().index.tolist():
        print(slugify(text=i[0], word_boundary=True, max_length=50))


print_article_info()

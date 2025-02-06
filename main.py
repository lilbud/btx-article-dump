import datetime
import json
import re
from pathlib import Path

import ftfy
import html2text
import httpx
import pandas as pd
import psycopg
from bs4 import BeautifulSoup as bs4
from dateparser import parse
from psycopg.rows import dict_row
from slugify import slugify
from thefuzz import process

base_folder = Path(Path(__file__).parent, "articles_orig")
sorted = Path(
    r"C:\Users\bvw20\Documents\Software\Programming\Python\Projects\btx-article-dump\articles_sorted",
)


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
    for folder in base_folder.iterdir():
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


def articles_to_db():
    articles = []

    # conn = psycopg.connect(
    #     "postgresql://postgres:password@localhost:5432/articledump",
    #     row_factory=dict_row,
    # )

    # cur = conn.cursor()

    for folder in base_folder.iterdir():
        # print(folder.name)
        for file in folder.iterdir():
            if file.suffix == ".md":
                try:
                    with Path.open(file, "r", encoding="utf-8") as f:
                        contents = "".join(f.readlines())
                except (UnicodeEncodeError, UnicodeDecodeError):
                    with Path.open(file, "r", encoding="cp1252") as f:
                        contents = "".join(f.readlines())

                title = re.search(r"title\: (.*)", contents)[1].strip('"')
                author = re.search(r"author\: (.*)", contents)[1].strip('"')
                source = re.search(r"source\: (.*)", contents)[1].strip('"')
                date = re.search(r"date\: (.*)", contents)[1].strip('"')
                category = re.search(r"category\: (.*)", contents)[1].strip('"')

                if date != "Unknown" and date != "Various":
                    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                else:
                    date = None

                # cur.execute(
                #     """INSERT INTO articles (category, date, source, author, title) VALUES (%s, %s, %s, %s, %s)""",
                #     [category, date, source, author, title],
                # )

                # conn.commit()


articles_to_db()

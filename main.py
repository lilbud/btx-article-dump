import re
from datetime import datetime
from pathlib import Path

import ftfy
import html2text
import pandas as pd
from slugify import slugify

base_folder = Path(Path(__file__).parent, "articles_orig")


def format_md(file: Path, h: html2text.HTML2Text) -> str:
    """Markdown format."""
    f = Path.open(file, encoding="utf-8")
    return h.handle(ftfy.fix_text("\n".join([line.strip() for line in f.readlines()])))


def html_to_md() -> None:
    """Parse through the original BTX html dumps and convert to markdown."""
    page = Path(
        r"Articles Thread",
    )

    h = html2text.HTML2Text()
    save = Path(Path(__file__).parent, "articles")

    for file in page.iterdir():
        if file.suffix == ".htm":
            formatted = format_md(file, h)

            with Path.open(Path(save, f"{file.stem}.md"), "w", encoding="utf-8") as f:
                f.write(formatted)


def unwrap_articles() -> None:
    """Unwrap article files from 80 char width."""
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


def article_metadata(contents: str) -> dict:
    """Pull article information from header."""
    meta = {}

    meta["title"] = re.search(r"title\: (.*)", contents)[1].strip('"')
    meta["author"] = re.search(r"author\: (.*)", contents)[1].strip('"')
    meta["source"] = re.search(r"source\: (.*)", contents)[1].strip('"')
    meta["date"] = re.search(r"date\: (.*)", contents)[1].strip('"')
    meta["category"] = re.search(r"category\: (.*)", contents)[1].strip('"')

    try:
        meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        meta["date"] = "Unknown"

    try:
        meta["subcategory"] = re.search(r"subcategory\: (.*)", contents)[1].strip('"')
    except TypeError:
        meta["subcategory"] = None

    return meta


def replace_album(album: str) -> str:
    """Fix incorrect article names."""
    match album:
        case "Greetings From Asbury Park, NJ":
            return "Greetings From Asbury Park, N.J."
        case "Born In The USA":
            return "Born In The U.S.A."
        case "Live 1975-1985":
            return "Live 1975-85"
        case "Devils and Dust":
            return "Devils & Dust"
        case "The Wild, The Innocent and The E Street Shuffle":
            return "The Wild, The Innocent & The E Street Shuffle"
        case _:
            return album


albums = [
    "Greetings From Asbury Park, N.J.",
    "Greetings From Asbury Park, NJ",
    "The Wild, The Innocent & The E Street Shuffle",
    "The Wild, The Innocent and The E Street Shuffle",
    "Born To Run",
    "Darkness On The Edge Of Town",
    "The River",
    "Nebraska",
    "Born In The U.S.A.",
    "Born In The USA",
    "Live 1975-85",
    "Live 1975-1985",
    "Tunnel Of Love",
    "Human Touch",
    "Lucky Town",
    "Greatest Hits",
    "The Ghost Of Tom Joad",
    "Tracks",
    "The Rising",
    "The Essential",
    "Devils & Dust",
    "Devils and Dust",
    "We Shall Overcome",
    "Magic",
    "Working On A Dream",
    "The Promise",
    "Wrecking Ball",
    "High Hopes",
    "The Ties That Bind",
    "Chapter And Verse",
    "Western Stars",
    "Letter To You",
    "Only The Strong Survive",
]


def article_renaming(folder: str) -> None:
    """Rename article file based on metadata."""
    for file in Path.glob(Path(sorted, folder), "**/*.md"):
        content = "\n".join([line.strip() for line in file.open().readlines()])

        meta = article_metadata(content)

        orig_name = re.sub(r"\_", "", file.stem)

        if meta["source"] == meta["author"]:
            new_name = f"{meta['date']}_{slugify(meta['author'])}"
        else:
            new_name = (
                f"{meta['date']}_{slugify(meta['author'])}_{slugify(meta['source'])}"
            )

        if not Path.exists(
            Path(file.parent, f"{new_name} [{orig_name}].md"),
        ):
            file.rename(
                f"{file.parent}\\{new_name} [{orig_name}].md",
            )
        else:
            print(file.name)


def article_sorting(folder: str) -> None:
    """Sort articles by category."""
    for file in base_folder.iterdir():
        content = "\n".join([line.strip() for line in file.open().readlines()])

        meta = article_metadata(content)

        if meta["category"] == folder:
            with Path.open(Path(sorted, folder, file.name), "w") as new_file:
                new_file.write(content)


def generate_sheet() -> None:
    """Generate .csv sheet of articles."""
    sheet = []

    for file in Path.glob(Path(r"articles"), "**/*.md"):
        content = "\n".join([line.strip() for line in file.open().readlines()])

        meta = article_metadata(content)

        page = re.search(r"\[(\d{3,4})\]", file.name)[1]

        current = list(meta.values())
        current.append(page)

        url = f"https://github.com/lilbud/btx-article-dump/blob/main/{Path(file.parent, file.name).as_posix()}"  # noqa: E501

        url = url.replace("[", "%5B").replace("]", "%5D")
        current.append(url)

        sheet.append(current)

    df = pd.DataFrame(sheet)

    df.columns = [
        "title",
        "author",
        "source",
        "date",
        "category",
        "subcategory",
        "page",
        "link",
    ]

    df = (
        df[
            [
                "page",
                "link",
                "author",
                "source",
                "title",
                "date",
                "category",
                "subcategory",
            ]
        ]
        .set_index("page")
        .sort_values("page")
    )

    df.to_csv("sheet.csv")


generate_sheet()

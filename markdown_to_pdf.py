import re
from datetime import datetime
from pathlib import Path

from markdown_pdf import MarkdownPdf, Section

file = Path(
    r".\\articles\\commentary\\1975-10-05_if_there_hadn_t_been_a_bruce_springsteen_[8206].md",
)


def article_metadata(contents: str) -> dict:
    """Pull article information from header."""
    meta = {}

    meta["title"] = re.search(r"title\: (.*)", contents)[1].strip('"')
    meta["author"] = re.search(r"author\: (.*)", contents)[1].strip('"')
    meta["source"] = re.search(r"source\: (.*)", contents)[1].strip('"')
    meta["date"] = re.search(r"date\: (.*)", contents)[1].strip('"')
    meta["category"] = re.search(r"category\: (.*)", contents)[1].strip('"')

    try:
        meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d")
    except ValueError:
        meta["date"] = "Unknown"

    return meta


print(file.parent.name)

with file.open("r") as f:
    content = [line.strip() for line in f.readlines()]

    meta = article_metadata("\n".join(content[0:7]))
    content = "".join([f"<p>{i}</p>" for i in content[7:]])

    pdf = MarkdownPdf(toc_level=2)

    pdf.add_section(
        Section(
            f"<h1>{meta['title']}</h1><h5>{meta['author']}</h5><h5>{meta['source']}</h5><h5>{meta['date'].strftime('%B %d, %Y')}</h5>\n\n{content}",
            toc=False,
        ),
        user_css="h5 {line-height: 0; } body {font-family: system-ui;}",
    )

    pdf.meta["modDate"] = meta["date"].strftime("%Y-%m-%d")
    pdf.meta["producer"] = meta["source"]
    pdf.meta["author"] = meta["author"]
    pdf.meta["title"] = meta["title"]

    pdf.save(Path(r".\\pdf", file.parent.name, f"{file.stem}.pdf"))

from pathlib import Path

from spellchecker import SpellChecker

spell = SpellChecker()

content = Path(
    r"C:\Users\bvw20\Documents\Software\Programming\Python\Projects\btx-article-dump\articles\commentary\1974-02-09_springsteen_turns_on_the_heat_[1001].md",
).read_text()

for i in content.split(" "):
    check = spell.correction(i)

    if check:
        print(check)

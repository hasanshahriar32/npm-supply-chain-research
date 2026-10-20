import glob
import re

for fpath in sorted(glob.glob("manuscript_q1/sections/*.tex")):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    orig = content
    content = content.replace("—", "---")
    content = content.replace("–", "--")
    lines = content.split("\n")
    new_lines = []
    in_tabular = False
    for line in lines:
        if "\\begin{tabular" in line:
            in_tabular = True
        elif "\\end{tabular" in line:
            in_tabular = False
        elif not in_tabular:
            # Replace & not preceded by \
            line = re.sub(r"(?<!\\)&", r"\&", line)
        new_lines.append(line)
    content = "\n".join(new_lines)
    if content != orig:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated:", fpath)

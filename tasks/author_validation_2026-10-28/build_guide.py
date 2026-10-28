"""Build the printable task guide from its Markdown source with Tectonic."""
from pathlib import Path
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent


def escape(text):
    table = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
             '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
             '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(table.get(c, c) for c in text)


def inline(text):
    parts = re.split(r'(`[^`]+`|\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*)', text)
    out = []
    for part in parts:
        if part.startswith('`'):
            out.append(r'\nolinkurl{' + part[1:-1] + '}')
        elif part.startswith('**'):
            out.append(r'\textbf{' + escape(part[2:-2]) + '}')
        elif part.startswith('['):
            match = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', part)
            out.append(r'\href{' + match[2] + '}{' + escape(match[1]) + '}')
        else:
            out.append(escape(part))
    return ''.join(out)


def main():
    lines = (HERE / 'Author_Validation_Guide.md').read_text().splitlines()
    result = []
    list_type = None
    code = False

    def close_list():
        nonlocal list_type
        if list_type:
            result.append(r'\end{' + list_type + '}')
            list_type = None

    for line in lines:
        if line.startswith('```'):
            close_list()
            code = not code
            result.append(r'\begin{lstlisting}' if code else r'\end{lstlisting}')
            continue
        if code:
            result.append(line)
            continue
        if line.startswith('# '):
            continue
        if line.startswith('## '):
            close_list()
            title = re.sub(r'^\d+\.\s*', '', line[3:])
            result.append(r'\section{' + escape(title) + '}')
        elif line.startswith('### '):
            close_list()
            title = re.sub(r'^\d+\.\d+\s*', '', line[4:])
            result.append(r'\subsection{' + escape(title) + '}')
        elif line.startswith('- ') or re.match(r'^\d+\. ', line):
            kind = 'itemize' if line.startswith('- ') else 'enumerate'
            if list_type != kind:
                close_list()
                result.append(r'\begin{' + kind + '}')
                list_type = kind
            result.append(r'\item ' + inline(re.sub(r'^(?:- |\d+\. )', '', line)))
        else:
            close_list()
            result.append(inline(line) + ('\n' if not line else ''))
    close_list()
    preamble = r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=24mm]{geometry}
\usepackage{xcolor,enumitem,listings,fancyhdr}
\usepackage[hidelinks]{hyperref}
\usepackage{xurl}
\hypersetup{pdftitle={Author Validation Task Guide},pdfauthor={Task instructions prepared with AI assistance for Shahriar Hasan and Md. Ashikul Islam}}
\definecolor{taskblue}{HTML}{173F5F}
\definecolor{taskpale}{HTML}{F3F6F8}
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}
\setlist{leftmargin=*,itemsep=3pt,topsep=4pt}
\lstset{basicstyle=\ttfamily\footnotesize,breaklines=true,columns=fullflexible,keepspaces=true,frame=single,rulecolor=\color{gray},backgroundcolor=\color{taskpale},xleftmargin=3pt,xrightmargin=3pt}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small Author validation task}
\fancyhead[R]{\small 28 October 2026}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\setcounter{tocdepth}{2}
\begin{document}
\begin{titlepage}
\vspace*{12mm}
{\color{taskblue}\Huge\bfseries Author validation\\[4pt]task guide\par}
\vspace{8mm}
{\Large Shahriar Hasan\\Md. Ashikul Islam\par}
\vspace{10mm}
{\large npm supply-chain research / EMSE manuscript\par}
\vspace{10mm}
\colorbox{taskpale}{\parbox{0.94\linewidth}{\textbf{Your deliverables}\\Two independent 120-row review sheets; documented resolution of disagreements; actual contribution descriptions; and each author's approval of the final manuscript.}}
\par
\vspace{8mm}
\textbf{Start here:} read Sections 1--7, open Evidence\_Index.html, then work independently in your own CSV. Do not compare initial decisions until both passes are complete and saved.
\vfill
Prepared 28 October 2026, Asia/Dhaka.\\
This document gives instructions. It does not record completed reviews or author approval. The endpoint audit is additional validation, not a journal-mandated procedure.
\end{titlepage}
\tableofcontents
\clearpage
'''
    target = HERE / 'Author_Validation_Guide.tex'
    target.write_text(preamble + '\n'.join(result) + '\n' + r'\end{document}' + '\n')
    compiler = shutil.which('tectonic') or str(Path.home() / '.local/bin/tectonic')
    build = HERE / 'build'
    build.mkdir(exist_ok=True)
    completed = subprocess.run([compiler, '--keep-logs', '--outdir', str(build), target.name],
                               cwd=HERE, text=True, capture_output=True)
    (build / 'compiler.txt').write_text(completed.stdout + completed.stderr)
    if completed.returncode:
        raise RuntimeError((completed.stdout + completed.stderr)[-5000:])
    shutil.copy2(build / 'Author_Validation_Guide.pdf', HERE / 'Author_Validation_Guide.pdf')
    print('Built', HERE / 'Author_Validation_Guide.pdf')


if __name__ == '__main__':
    main()

#!/bin/bash
mkdir -p build/

# Compile research paper
pdflatex -output-directory build/ -jobname research-paper docs/research-paper.tex
pdflatex -output-directory build/ -jobname research-paper docs/research-paper.tex

#!/bin/bash
mkdir -p dist/docs

# Compile implementation
npx tsc

# Compile research paper
pdflatex -output-directory dist/docs -jobname research-paper docs/research-paper.tex
pdflatex -output-directory dist/docs -jobname research-paper docs/research-paper.tex


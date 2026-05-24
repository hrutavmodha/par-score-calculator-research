#!/bin/bash
# Compilation script for the research paper

# Ensure the output directory exists
mkdir -p dist/docs

# Run pdflatex twice to ensure TOC and references are populated
pdflatex -output-directory dist/docs -jobname research-paper docs/research-paper.tex
pdflatex -output-directory dist/docs -jobname research-paper docs/research-paper.tex

echo "Compilation complete. Output located at dist/docs/research-paper.pdf"

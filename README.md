# Lexical-Word-Expansion-Using-NLP
This repository contains an NLP pipeline for lexical word expansion using BERT, WordNet, and FastText. The project automates the word generation process to enhance large-scale NLP tasks.

Overview
This project implements multiple NLP models to generate similar words for a given list of seed words. The goal is to improve lexical expansion using various techniques:

BERT: Uses pre-trained embeddings to find semantically similar words.
FastText: Generates similar words based on word embeddings.
WordNet: Finds synonyms and related words using linguistic databases.
Duplicate Removal: Ensures unique lexical words across all algorithms.

Usage
1. Running FastText Model
python fasttext_model.py
A seed word input file (Excel format).
A FastText model file.

3. Running WordNet Model
python wordnet_model.py
This script generates lexical words using WordNet.

4. Removing Duplicates
python Removing_duplicates.py
This script removes duplicate words within and across algorithms.

Expected Output
Each script generates an Excel file with lexical words for each seed word, categorized by theme.

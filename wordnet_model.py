import nltk
from nltk.corpus import wordnet as wn
import pandas as pd
import os


# Dowloading required models for wordnet
nltk.download('wordnet')
nltk.download('omw-1.4')

# generating lexical words
def find_related_words_for_phrases(seed_words):
    """
    Finds related words for a list of phrases using WordNet synsets.

    Args:
    seed_words (list): A list of seed words or phrases for which related words need to be found.

    Returns:
    dict: A dictionary where keys are phrases and values are lists of lexical words.
    """
    results = {}
    for phrase in seed_words:
        words = phrase.split()  # Spliting the phrase into individual words
        related_words = set()
        for word in words:
            synsets = wn.synsets(word)  # Getting synsets (sets of synonyms) for the word from WordNet
            for syn in synsets:
                for lemma in syn.lemmas():
                    related_words.add(lemma.name().replace('_', ' ')) # Add the lemma's name to the related_words set
        if related_words:
            results[phrase] = list(related_words)
        else:
            results[phrase] = ["No related words found in WordNet."]
    return results


# Creating dataframe of generated lexical words with seed word as column name and its respective lexical words as rows.
def to_dataframe(results):
    df = pd.DataFrame.from_dict(results, orient='index').transpose()
    return df

# Creating main function to call all the above created functions.
def main(input_file_path,output_dir):
    input_df=pd.read_excel(input_file_path)
    for theme in input_df.columns:
        seed_words=input_df[theme].dropna().tolist()
        closest_words = find_related_words_for_phrases(seed_words)
        df = to_dataframe(closest_words)
        output_file = os.path.join(output_dir, f"{theme}_wordnet_lexical_words.xlsx")
        df.to_excel(output_file,index=False)


# Change the below file paths according to your folder path
input_file_path='D:/Sarvesh/Model/Model_Seed_words_Input_file.xlsx' # file path to take the seed words as input.
output_dir='D:/Sarvesh/Model/OUTPUT' # file path to save the lexical words generated in each of the theme.


# Run the main function
main(input_file_path,output_dir)
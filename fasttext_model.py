import gensim
import pandas as pd
import numpy as np
import os

# crreating Fasttext model
def fasttext_model(model_path):
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=False)
    return model


# generaating lexical words with decided threshold
def lexical_words(model, seed_word_list,threshold=0.7):
    """
    Finds lexical words similar to seed phrases using a given model.

    Args:
    model: Word embedding model (FastText) that supports word lookup and similarity.
    seed_word_list (list): A list of seed words or phrases for which similar words need to be found.
    threshold (float): A similarity threshold to filter out words.

    Returns:
    dict: A dictionary where keys are seed phrases and values are lists of related words.
    """
    results = {}
    for phrase in seed_word_list:
        words = phrase.split()   # Spliting the phrase into individual words
        if all(word in model for word in words):
            average_vector = np.mean([model[word] for word in words], axis=0) # Calculating the average vector of all words in the phrase
            similar_words = model.similar_by_vector(average_vector, topn=100)  #first taking 100 words similar to given seed word or phrase.
            relevant_words = []
            for word, similarity in similar_words:  #comparing similarity score with the given threshold  
                if similarity >= threshold:
                    relevant_words.append(word)
            results[phrase] = relevant_words
        else:
            results[phrase] = ["Not found in model"] *100
    return results


# Creating dataframe of generated lexical words with seed word as column name and its respective lexical words as rows.
def to_dataframe(results):
df = pd.DataFrame.from_dict(results, orient='index').transpose()
return df


# Creating main function to call all the above created functions.
def main(model_path,input_file_path,output_dir):
    model = fasttext_model(model_path)
    input_df=pd.read_excel(input_file_path)
    for theme in input_df.columns:
        seed_words=input_df[theme].dropna().tolist()
        closest_words = lexical_words(model, seed_words)
        df = to_dataframe(closest_words)
        output_file = os.path.join(output_dir, f"{theme}_fasttext_lexical_words.xlsx")
        df.to_excel(output_file,index=False)

# Change the below file paths according to your folder path
input_file_path='D:/Sarvesh/Model/Model_Seed_words_Input_file.xlsx' # file path to take the seed words as input.
model_path = 'D:/Sarvesh/Model/wiki-news-300d-1M-subword.vec/wiki-news-300d-1M-subword.vec' # file path for fasttext model downloaded.
output_dir='D:/Sarvesh/Model/OUTPUT/Raw_Output' # file path to save the lexical words generated in each of the theme.

# Run the main function
main(model_path,input_file_path,output_dir)
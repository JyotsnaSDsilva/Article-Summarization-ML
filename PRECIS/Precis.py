from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import re


MAX = 7

def _create_dictionary_table(text_string) -> dict:
   
    # Removing stop words
    stop_words = set(stopwords.words("english"))
    
    words = word_tokenize(text_string)
    
    # Reducing words to their root form
    stemmer = PorterStemmer()
    
    # Creating dictionary for the word frequency table
    frequency_table = dict()
    for word in words:
        word = stemmer.stem(word)
        if word in stop_words:
            continue
        if word in frequency_table:
            frequency_table[word] += 1
        else:
            frequency_table[word] = 1

    return frequency_table


def _calculate_sentence_scores(sentences, frequency_table) -> dict:   

    # Algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        #sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:MAX] in sentence_weight:
                    sentence_weight[sentence[:MAX]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:MAX]] = frequency_table[word_weight]

        sentence_weight[sentence[:MAX]] = sentence_weight[sentence[:MAX]]/sentence_wordcount_without_stop_words
      
    return sentence_weight


def _calculate_average_score(sentence_weights) -> int:
   
    # Calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weights:
        sum_values += sentence_weights[entry]

    try:
        # Getting sentence average value from source text
        average_score = (sum_values / len(sentence_weights))
        return average_score
    except:
        return 0


def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:MAX] in sentence_weight and sentence_weight[sentence[:MAX]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary


def set_threshold(threshold):
  range_Series = [0,11,25,35,50,61,101,201,301,401,501,10000] #all the range values mentioned here
  values = [1,1.1,1.3,1.4,1.5,1.6,1.7,2,3,4,5] #values
  th = int(threshold)
  for i in range(len(range_Series)-1):
        if th in range(range_Series[i],range_Series[i+1]):
            #print("mul : ", values[i])
            return (float)(threshold * values[i])


def _run_article_summary(article):
    
    frequency_table = _create_dictionary_table(article)
    sentences = sent_tokenize(article)
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)
    threshold = _calculate_average_score(sentence_scores)
    #print(threshold)
    
    if threshold == 0:
        return "No Content Found that could be summarized. Make sure the input is Correct."

    #producing the summary
    article_summary = _get_article_summary(sentences, sentence_scores, set_threshold(threshold))

    result_summary = re.sub(r"\[\d+\]", "",article_summary)

    if len(article) <= len(result_summary):
        return "Article is not suitable to be summarized"

    print('length of original article : ', len(article),'\n length of summary : ',len(result_summary))

    return result_summary


    
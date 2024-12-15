from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
import pandas as pd
from scipy.special import softmax
from tools import progress

# Preprocess text (username and link placeholders)
def preprocess(text): ### TO UPDATE WITH GOOD PREPROCESSING (remove only username comments, and treat separately comments that are too long).
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t #normalize users
        t = 'http' if t.startswith('http') else t #normalize links
        #we could also want to treat emojis. idk how the model handles them really (quite impressed it handles them in any way)
        new_text.append(t)
    return " ".join(new_text)


def setup_model(MODEL="cardiffnlp/twitter-xlm-roberta-base-sentiment"): #defaults to the non-finetuned model.
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)

    # PT
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    model.save_pretrained(MODEL)
    tokenizer.save_pretrained(MODEL)

    return model, tokenizer, config



def analyze_comment(comment, model, tokenizer):

    try:
        n = len(comment)
    except:
        print("\n")
        print(comment)
        print(type(comment))
    if n > 500: #max size for single text comment is 514. If comment is too long, we split it in as many pieces in necessary then compute the mean of the sub scores.
        expand_comment = [comment[500*i:500*(i+1)] for i in range((500 // n) + 1 + 1)]
        sub_scores=[]
        for sub_comment in expand_comment: 
            sub_comment = preprocess(sub_comment)
            encoded_input = tokenizer(sub_comment, return_tensors='pt')
            output = model(**encoded_input)
            scores = output[0][0].detach().numpy()
            sub_scores.append(softmax(scores))
        scores = np.array( [np.mean([el[i] for el in sub_scores]) for i in range(3)] ) #ugly and inefficient, but working.

    else: #regular processing if length is ok.
        comment = preprocess(comment)
        encoded_input = tokenizer(comment, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

    return scores


def analyze_all_comments(dataset, model, tokenizer): #this function is not used outside of the example. The thing is that the datset changes form between tiktok, youtube and reddit...
    scores_dict = {}
    for comment in dataset:
        scores = analyze_comment(comment, model, tokenizer)
        scores_dict[comment] = scores

    return scores_dict


def analyze_tiktok_comments(dataset, model, tokenizer, config):

    keys, positives, neutrals, negatives = [], [], [], []
    n=dataset.shape[0] #nb of lines
    for i, (text, key) in dataset.iterrows():
        scores_dict = {} #will contain score for positive, neutral and negative.

        scores = analyze_comment(text, model, tokenizer)
        #scores_dict[(url,id)] = scores #(url,id) is a unique identifier for each comment. Will be necessary for the final join.

        #rank scores - separate function for this ?
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for j in range(scores.shape[0]):
            l = config.id2label[ranking[j]]
            s = scores[ranking[j]]

            scores_dict[l] = np.round(float(s), 2)

        keys.append(key)
        try: #if original model
            positives.append(scores_dict["positive"])
            neutrals.append(scores_dict["neutral"])
            negatives.append(scores_dict["negative"])
        except: #if finetuned model
            positives.append(scores_dict['2'])
            neutrals.append(scores_dict['1'])
            negatives.append(scores_dict['0'])
        #

        progress(int( ((i+1)/n)*100) )

    d = {'join_key':keys, 'positive':positives,'neutral':neutrals, 'negative':negatives}
    scores_df = pd.DataFrame(data = d)

    return scores_df


def analyze_youtube_comments(dataset, model, tokenizer, config):
    keys, positives, neutrals, negatives = [], [], [], []
    n=dataset.shape[0] #nb of lines
    for i, (text, key) in dataset.iterrows():
        scores_dict = {} #will contain score for positive, neutral and negative.

        scores = analyze_comment(text, model, tokenizer)
        #scores_dict[(url,id)] = scores #(url,id) is a unique identifier for each comment. Will be necessary for the final join.

        #rank scores - separate function for this ?
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for j in range(scores.shape[0]):
            l = config.id2label[ranking[j]]
            s = scores[ranking[j]]

            scores_dict[l] = np.round(float(s), 2)

        keys.append(key)
        try:
            positives.append(scores_dict["positive"])
            neutrals.append(scores_dict["neutral"])
            negatives.append(scores_dict["negative"])
        except:
            positives.append(scores_dict['2'])
            neutrals.append(scores_dict['1'])
            negatives.append(scores_dict['0'])

        #

        progress(int( ((i+1)/n)*100) )

    d = {'join_key':keys, 'positive':positives,'neutral':neutrals, 'negative':negatives}
    scores_df = pd.DataFrame(data = d)

    return scores_df


def analyze_reddit_comments(dataset, model, tokenizer, config):
    keys, positives, neutrals, negatives = [], [], [], []
    n=dataset.shape[0] #nb of lines
    for i, (text,join_key) in dataset.iterrows():
        scores_dict = {} #will contain score for positive, neutral and negative.

        scores = analyze_comment(text, model, tokenizer)
        #scores_dict[(url,id)] = scores #(url,id) is a unique identifier for each comment. Will be necessary for the final join.

        #rank scores - separate function for this ?
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for j in range(scores.shape[0]):
            l = config.id2label[ranking[j]]
            s = scores[ranking[j]]

            scores_dict[l] = np.round(float(s), 2)

        keys.append(join_key)
        try:
            positives.append(scores_dict["positive"])
            neutrals.append(scores_dict["neutral"])
            negatives.append(scores_dict["negative"])
        except:
            positives.append(scores_dict['2'])
            neutrals.append(scores_dict['1'])
            negatives.append(scores_dict['0'])
        #

        progress(int( ((i+1)/n)*100) )


    d = {'join_key':keys, 'positive':positives,'neutral':neutrals, 'negative':negatives}
    scores_df = pd.DataFrame(data = d)

    return scores_df


def test():

    # MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual"
    # MODEL = f"Lyreck/finetune-tiktok-brat7" #finetuned model with small dataset
    MODEL = f"Lyreck/brat-summer_256comms" #finetuned model with slightly larger dataset
    model, tokenizer, config = setup_model(MODEL)

    text = "she ate this"
    #text = "i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love youi love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you"
    #"]

    scores_dict = analyze_all_comments([text], model, tokenizer)

    for comment in scores_dict.keys():
        scores = scores_dict[comment]

        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for i in range(scores.shape[0]):
            l = config.id2label[ranking[i]]
            s = scores[ranking[i]]
            print(f"{i+1}) {l} {np.round(float(s), 4)}")



if __name__ == "__main__":
    test()
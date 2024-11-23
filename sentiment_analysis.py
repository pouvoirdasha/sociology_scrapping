from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax

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

    n = len(comment)
    if len(comment) > 500: #max size for single text comment is 514. If comment is too long, we split it in as many pieces in necessary then compute the mean of the sub scores.
        expand_comment = [comment[500*i:500*(i+1)] for i in range((500 // n) + 1 + 1)]
        sub_scores=[]
        for sub_comment in expand_comment: 
            sub_comment = preprocess(sub_comment)
            encoded_input = tokenizer(sub_comment, return_tensors='pt')
            output = model(**encoded_input)
            scores = output[0][0].detach().numpy()
            sub_scores.append(softmax(scores))
        print(f'list of sub scores (to see la gueule du truc): {sub_scores}')
        scores = np.array( [np.mean([el[i] for el in sub_scores]) for i in range(3)] ) #ugly and inefficient, but working.

    else: #regular processing if length is ok.
        comment = preprocess(comment)
        encoded_input = tokenizer(comment, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

    return scores

def analyze_all_comments(dataset, model, tokenizer): #arg dataset à préciser
    scores_dict = {}
    for comment in dataset:
        scores = analyze_comment(comment, model, tokenizer)
        scores_dict[comment] = scores

    return scores_dict


def test():

    MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual"
    # MODEL = f"Lyreck/finetune-tiktok-brat6" #finetuned model 
    model, tokenizer, config = setup_model(MODEL)

    #text = "kamala is brat"
    text = "i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love youi love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you i love you"

    scores_dict = analyze_all_comments([text], model, tokenizer)

    for comment in scores_dict.keys():
        scores = scores_dict[comment]

        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for i in range(scores.shape[0]):
            l = config.id2label[ranking[i]]
            s = scores[ranking[i]]
            print(f"{i+1}) {l} {np.round(float(s), 4)}")



########## Pour gérer l'affichage des scores ##########@
# Print labels and scores
# ranking = np.argsort(scores)
# ranking = ranking[::-1]
# for i in range(scores.shape[0]):
#     l = config.id2label[ranking[i]]
#     s = scores[ranking[i]]
#     print(f"{i+1}) {l} {np.round(float(s), 4)}")
######### à voir en fonction de la gueuel eque prned notre dataset de commentaires. Probablement devoir rajouter 
# des infos sur chaque commentaire pour avoir un identifiant unique?


# # TF
# model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)
# model.save_pretrained(MODEL)

# text = "Good night 😊"
# encoded_input = tokenizer(text, return_tensors='tf')
# output = model(encoded_input)
# scores = output[0][0].numpy()
# scores = softmax(scores)


if __name__ == "__main__":
    test()
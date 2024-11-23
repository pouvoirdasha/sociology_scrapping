import datetime
date = datetime.datetime.now() #to name files with date
import os
import pandas as pd
from IPython.display import display

from youtube_comments_scraping import scrape_youtube_videos
from fusion_tiktok_datasets import read_tiktok_excel, concatAllTikTok
from sentiment_analysis import analyze_comment, setup_model
from tools import progress_bar


def main():
    #choose which code segments you want to execute.
    youtube=False
    tiktok=False
    sentiment_analysis=True

    ##############################################################################################################################################################################
    ########################################################################## YOUTUBE COMMENT SCRAPING ##########################################################################
    
    if youtube:
        out = True
        out_filename= f"YouTube-comments_{date.day}-{date.month}-{date.year}_{date.hour}h{date.minute}.csv"
        yt_ids_to_scrape = [
            "Js4qqwdjA9M", #549 
            "fxv-YhT3Ixc", #165
            "EWUK5A-3LSI", #862
            "y4BKfR5t1l8", #427
            "8zPor9l9SwI", #11 838 #WILL CAP THE COMMENTS LIMIT !
            "w1u9IgepfAU", #393
            "YF7Hs4GeJkQ", #1 700
            "1EuF7yfoyDE"  #2 372
        ]

        # yt_ids_to_scrape=["Awfy38D90gk"] #for debugging/test


        comments = scrape_youtube_videos(yt_ids_to_scrape,out_filename,out)

        print(f"Actual Number of YouTube comments: {len(comments)}. | Expected number of YouTube comments= {549+165+862+427+393+1700+2372+11838}") #+11838 avec la grosse vidéo.


    ##############################################################################################################################################################################
    ########################################################################## MERGE TIKTOK EXCEL FILES ##########################################################################

    if tiktok:
        dir_to_tiktok_files = "data/tiktok_comments/"
        tiktok_excel_files = []
        
        for tiktok_filename in os.listdir(dir_to_tiktok_files):
            tiktok_file = read_tiktok_excel(dir_to_tiktok_files + tiktok_filename)
            tiktok_excel_files.append(tiktok_file)

        out = True
        out_filename= f"TikTok-comments_{date.day}-{date.month}-{date.year}_{date.hour}h{date.minute}.csv"

        concatenated_tiktok = concatAllTikTok(out, out_filename, *tiktok_excel_files)

        print(f"Merged together {concatenated_tiktok.shape[0]} TikTok Comments")


    ##############################################################################################################################################################################
    ############################################################################# SENTIMENT ANALYSIS #############################################################################

    # il faut que les commentaires soient donnés et analysés dans un ordre spécifique, afin que l'on puisse rajouter la colonne aux datasets et ainsi analyser les données
    # dans leur ensemble.

    if sentiment_analysis:

        ## initialize model
        MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual"
        model, tokenizer, config = setup_model(MODEL)

        ## get data
        tiktok_file = "./results/TikTok-comments_18-11-2024_12h46.csv"
        tiktok_comments = pd.read_csv(tiktok_file)
        tiktok_comments = tiktok_comments[["Comment Text", "post_url", "Comment Number (ID)"]] #key = (post_url, Comment Number (ID)).
            

        ## analyze data
        scores_dict = {} #analyzing one by one seems more natural here (even if I made a general analyze_all_comments function !!)
        for i, (text, url, id) in tiktok_comments.iterrows():
            scores = analyze_comment(text, model, tokenizer)
            scores_dict[(url,id)] = scores #(url,id) is a unique identifier for each comment. Will be necessary for the final join.

        print(scores_dict)

        ## add columns do data frames.









if __name__ == "__main__":
    main()
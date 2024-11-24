import datetime
date = datetime.datetime.now() #to name files with date
import os
import pandas as pd
from IPython.display import display

from youtube_comments_scraping import scrape_youtube_videos
from fusion_tiktok_datasets import read_tiktok_excel, concatAllTikTok
from sentiment_analysis import setup_model, analyze_tiktok_comments, analyze_youtube_comments, analyze_reddit_comments
from tools import progress


def main():
    #choose which code segments you want to execute.
    youtube=False
    tiktok=False
    tiktok_sentiment_analysis=False
    youtube_sentiment_analysis=True
    reddit_sentiment_analysis=False

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

    ## initialize model
    # MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual" #original model
    MODEL = f"Lyreck/finetune-tiktok-brat7" #finetuned model
    model, tokenizer, config = setup_model(MODEL)

    if tiktok_sentiment_analysis:

        print('--------------------------------------')
        print('Launching analysis of TikTok comments')
        ## get data
        tiktok_file = "./results/TikTok-comments_18-11-2024_12h46.csv"
        tiktok_df = pd.read_csv(tiktok_file)
        tiktok_df["join_key"] = [i for i in range(tiktok_df.shape[0])]
        tiktok_comments = tiktok_df[["Comment Text", "join_key"]] #key = join_key.

        ## analyze data
        scores_df = analyze_tiktok_comments(tiktok_comments, model, tokenizer, config)
        print("\n")

        ## add columns do data frames. (big merge !)
        tiktok_with_sentiments = pd.merge(tiktok_df, scores_df, how = 'inner', on='join_key')
        out_filename= f"TikTok-with-sentiments_{date.day}-{date.month}-{date.year}_{date.hour}h{date.minute}.csv"

        ## export to file
        out=True
        if out:
            tiktok_with_sentiments.to_csv("results/" + out_filename)
            print(f'Saved sentiment analysed TikTok comments to "results/{out_filename}".')


    if youtube_sentiment_analysis:

        print('---------------------------------------')
        print('Launching analysis of YouTube comments')

        ## get data
        youtube_file = "./results/youtube_comments.csv"
        youtube_df = pd.read_csv(youtube_file)
        youtube_df.dropna(axis='index', subset="Comment", inplace=True) #ça devrait être dans le prétratiement mais je mets un pansement ici car apparemment il reste du nan...
        youtube_df["join_key"] = [i for i in range(youtube_df.shape[0])]
        youtube_comments = youtube_df[["Comment", "join_key"]] #unique key to identify a comment: (VideoID, Username, Timestamp).

        ## analyze data
        scores_df = analyze_youtube_comments(youtube_comments, model, tokenizer, config)
        print('\n')

        ## add columns do data frames. (big merge !)
        youtube_with_sentiments = pd.merge(youtube_df, scores_df, how = 'inner', on="join_key")
        out_filename= f"YouTube-with-sentiments_{date.day}-{date.month}-{date.year}_{date.hour}h{date.minute}.csv"

        ## export to file
        out=True
        if out:
            youtube_with_sentiments.to_csv("results/" + out_filename)
            print(f'Saved sentiment analysed YouTube comments to "results/{out_filename}".')

    if reddit_sentiment_analysis:

        print('---------------------------------------')
        print('Launching analysis of Reddit comments')

        #### Il FAUT ECRIRE UN TRAITEMENT POUR REDDIT......... Là avec le format qu'on a pour l'instant c pas top. Pour l'instant j'ai un truc fait à la main, SANS URL.

        ## get data
        reddit_file = "./data/reddit.csv"
        reddit_df = pd.read_csv(reddit_file)
        reddit_df["join_key"] = [i for i in range(reddit_df.shape[0])]
        reddit_comments = reddit_df[["comment_content", "join_key"]] #unique key to identify a comment: just the text (I was reluctant to do this but the dataset lacks a unique key).

        ## analyze data
        scores_df = analyze_reddit_comments(reddit_comments, model, tokenizer, config)
        print('\n')

        ## add columns do data frames. (big merge !)
        reddit_with_sentiments = pd.merge(reddit_df, scores_df, how = 'inner', on=["join_key"])
        out_filename= f"Reddit-with-sentiments_{date.day}-{date.month}-{date.year}_{date.hour}h{date.minute}.csv"

        ## export to file
        out=True
        if out:
            reddit_with_sentiments.to_csv("results/" + out_filename)
            print(f'Saved sentiment analysed Reddit comments to "results/{out_filename}".')









if __name__ == "__main__":
    main()
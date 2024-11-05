import datetime
date = datetime.datetime.now() #to name files with name
import os

from youtube_comments_scraping import scrape_youtube_videos

from fusion_tiktok_datasets import read_tiktok_excel, concatAllTikTok


def main():

    ##############################################################################################################################################################################
    ########################################################################## YOUTUBE COMMENT SCRAPING ##########################################################################
    

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

    #yt_ids_to_scrape=["Awfy38D90gk"] #for debugging


    #comments = scrape_youtube_videos(yt_ids_to_scrape,out_filename,out)

    # print(f"Actual Number of YouTube comments: {len(comments)}. | Expected number of YouTube comments= {549+165+862+427+393+1700+2372+11838}") #+11838 avec la grosse vidéo.


    ##############################################################################################################################################################################
    ########################################################################## MERGE TIKTOK EXCEL FILES ##########################################################################

    dir_to_tiktok_files = "data/tiktok_comments/"
    tiktok_excel_files = []
    
    for tiktok_filename in os.listdir(dir_to_tiktok_files):
        tiktok_file = read_tiktok_excel(dir_to_tiktok_files + tiktok_filename)
        tiktok_excel_files.append(tiktok_file)

    out = True
    out_filename= f"TikTok-comments_{date.day}-{date.month}-{date.year}_{date.hour}h{date.minute}.csv"

    concatenated_tiktok = concatAllTikTok(out, out_filename, *tiktok_excel_files)

    print(f"Merged together {concatenated_tiktok.shape[0]} TikTok Comments")













if __name__ == "__main__":
    main()
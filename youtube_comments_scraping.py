##### Scrape YouTube comments from a given youtube video

# documentation source: https://developers-dot-devsite-v2-prod.appspot.com/youtube/v3/code_samples/code_snippets_a4196ae5378e1e8e3601e8aa898aca07716d4d415abf2b19bdd8ec6871fda96b.frame?hl=fr#
# also thanks to https://github.com/analyticswithadam/Python/blob/main/Pull_all_Comments_and_Replies_for_YouTube_Playlists.ipynb for showing how to get ALL comments.


# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import csv

import googleapiclient.discovery



def get_dev_key():
    with open('data/dev_key.txt', newline='') as devkeyfile:
        devkey = devkeyfile.readline()

    return devkey

def initialize_youtube_api():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = get_dev_key()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    return youtube


def scrape_comments_from_video(videoId, youtube):
    """Returns all comments from videoId in a json format.

    Args:
        videoId (str): ID of the video (found after v=..... in the video's URL)
        youtube (_type_): instance of Google's YouTube API to collect comments.

    Returns:
        json: response to the request (comments in json format).
    """
    next_page_token = None
    CONTINUER=True
    next_page_token=None
    all_comments = []

    while CONTINUER:

        request = youtube.commentThreads().list(
            part="snippet,replies",    #,replies",
            order="time",
            videoId=videoId,
            pageToken=next_page_token,
            textFormat="plainText"
        )
        #maxResults=100, 
        response = request.execute()

        all_comments = process_json(response, all_comments, videoId) #process json data and put it in a list

        #go to next page of results to get *all* comments.
        next_page_token = response.get('nextPageToken')
        CONTINUER = 'nextPageToken' in response

    return all_comments


def process_json(response, all_comments, videoId): #function inspired from https://github.com/analyticswithadam/Python/blob/main/Pull_all_Comments_and_Replies_for_YouTube_Playlists.ipynb 
    """Append comments (and related answers) contained in response to the list containing all comments. videoId is specified to track where the comments come from.

    Args:
        response (json): _description_
        all_comments (list): _description_
        videoId (str): _description_

    Returns:
        list: all_comments list to which was appended all the comments contained in the API response.
    """

    for item in response['items']:
            comment = item['snippet']["topLevelComment"]["snippet"]             #A VOIR ICI pour si on peut récup replies par la mm occasion avec l'argument "replies"
            all_comments.append({
                'Timestamp': comment['publishedAt'],
                'Username': comment['authorDisplayName'],
                'VideoID': videoId,
                'Comment': comment['textDisplay'],
                'Date': comment['updatedAt'] if 'updatedAt' in comment else comment['publishedAt'],
                'Modified': True if 'updatedAt' in comment else False,
                'NbLikes': comment['likeCount']
            })


            if "replies" in item: #s'il y a des réponses au commentaire "père" on les récupère aussi.
                replies = item['replies']['comments']
                for comment in replies:
                    comment = comment['snippet']
                    all_comments.append({
                        'Timestamp': comment['publishedAt'],
                        'Username': comment['authorDisplayName'],
                        'VideoID': videoId,
                        'Comment': comment['textDisplay'],
                        'Date': comment['updatedAt'] if 'updatedAt' in comment else comment['publishedAt'],
                        'Modified': True if 'updatedAt' in comment else False,
                        'NbLikes': comment['likeCount']
                    })

    return all_comments


def write_to_csv(comments:list, out_filename:str):

    with open("results/"+out_filename, 'w') as fichier: #remettre le fichier de résultats à 0 pour éviter de mélanger.
        fichier_writer = csv.writer(fichier, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        header = comments[0].keys()# ['Timestamp', 'Username', 'VideoID', 'Comment', 'Date', 'Modified', 'NbLikes']
        print(header)
        print(comments[0].values())
        fichier_writer.writerow(header)

    with open("results/"+out_filename, 'a', encoding = 'utf-8') as fichier:
            fichier_writer = csv.writer(fichier, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for comment in comments:
                fichier_writer.writerow(comment.values())


def scrape_youtube_videos(ids_to_scrape, out_filename, out):
    #ids_to_scrape contains all video ids that we wanna scrape.
    comments=[]

    youtube = initialize_youtube_api() #initialize scraper (api key, etc)

    print("==================== Beginning YouTube Scraping... ==================== \n")
    n=len(ids_to_scrape)
    for i,videoId in enumerate(ids_to_scrape):
        comments += scrape_comments_from_video(videoId, youtube) 
        progress(int(i+1/n*100))
    print('\n')

    if out:
        write_to_csv(comments,out_filename)
        print(f'\n Wrote results to "results/{out_filename}"')

    print(f'Number of comments (including answers) scraped: {len(comments)}.')
    print("\n ==================== Scraping done. ====================")

    return comments



def progress(percent=0, width=30): #simple progress bar
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)




def test_codes(): #test with a mininmal video.

     ###################### TO MODIFY DEPENDING ON USE ######################
    ## define name of file returned (if anything is returned at all)
    out = True
    out_filename= "YouTube-minimal-test.csv"

    ## define videos to scrape
    # videoIds_to_scrape =   ["Js4qqwdjA9M"]  # TO COMPLETE
    videoIds_to_scrape = ["Awfy38D90gk"] #test video with only 6 coms (2 of them being replies)
    ###################### TO MODIFY DEPENDING ON USE ######################


    comments = scrape_youtube_videos(videoIds_to_scrape,out_filename,out)




if __name__ == "__main__":
    test_codes()
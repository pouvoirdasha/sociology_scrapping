##### Scrape YouTube comments from a given youtube video

# documentation source: https://developers-dot-devsite-v2-prod.appspot.com/youtube/v3/code_samples/code_snippets_a4196ae5378e1e8e3601e8aa898aca07716d4d415abf2b19bdd8ec6871fda96b.frame?hl=fr#

# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import csv

import googleapiclient.discovery


#protect API key (you can create your own at https://console.cloud.google.com/apis/api/youtube.googleapis.com
with open('data/dev_key.txt', newline='') as devkeyfile:
    devkey = devkeyfile.readline()
print(devkey[0])


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
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=videoId,
        prettyPrint=True
    )
    response = request.execute()

    return response

def process_json(response):
    pass

def write_to_csv(data:list, out_filename:str):

    with open(out_filename, 'a', encoding = 'utf-8') as fichier:
            fichier_writer = csv.writer(fichier, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fichier_writer.writerow(data)

def main():

    ###################### TO MODIFY DEPENDING ON USE ######################
    ## define name of file returned (if anything is returned at all)
    out = True
    out_filename= "youtube_scraped_comments.csv"

    ## define videos to scrape
    videoIds_to_scrape = ["Js4qqwdjA9M"]  # TO COMPLETE
    ###################### TO MODIFY DEPENDING ON USE ######################

    ## initialize scraper
    youtube = initialize_youtube_api()

    ## scrape comments
    for videoId in videoIds_to_scrape:
        response = scrape_comments_from_video(videoId, youtube)
        processed_response = process_json(response)
        if out:
            write_to_csv(processed_response, out_filename)



if __name__ == "__main__":
    main()
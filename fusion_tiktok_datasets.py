###### Code pour fusionner deux fichiers excel renvoyés par la méthode de scrapping TikTok

import pandas as pd
import csv
from IPython.display import display
from datetime import datetime, timedelta #to get scraped date


def read_tiktok_excel(path:str):
    """read excel file and create associated pandas dataframe.

    Args:
        path (str): path to excel file (should look like "data/123456.xlsx")

    Returns:
        pandas dataframe: corresponding pandas dataframe, with an additional column ("post_url")
    """
    ## path = path to excel file (should be "data/123456.xlsx").

    df = pd.read_excel(path, index_col=0, skiprows=lambda x: x in [i for i in range(14)]) #skip 14 premières lignes qui contiennent metadata.

    ### recover intersting metadata on the post (url of post)

# I am keeping your code here in case : 
    #df_posturl = list(pd.read_excel(path, skiprows=[0], nrows=0))
    #df_posturl = df_posturl[1]
    #df['post_url'] = [df_posturl for _ in range(df.shape[0])] # add new column to df
    
    #recovering first few lines 
    df_metadata = pd.read_excel(path, usecols = [0,1],nrows=13)
    url = df_metadata.iloc[0,1]
    nb_coms_shown = df_metadata.iloc[11,1]
    nb_com_scraped = df_metadata.iloc[10,1]
    diff = df_metadata.iloc[12,1]
    publisher = df_metadata.iloc[2,1]
    post_likes = df_metadata.iloc[5,1]
    post_shares = df_metadata.iloc[6,1]
    post_description = df_metadata.iloc[7,1]

    format = "%b %d %Y"
    date_scraped = datetime.strptime(df_metadata.columns[1][4:15], format) #moche mais bon...


    df['post_url'] = [url for _ in range(df.shape[0])]
    df['shown_comments']= [nb_coms_shown for _ in range(df.shape[0])]
    df['scraped_comments']= [nb_com_scraped for _ in range(df.shape[0])]
    df['difference']= [diff for _ in range(df.shape[0])]
    df['publisher'] = [publisher for _ in range(df.shape[0])]
    df['post_likes'] = [post_likes for _ in range(df.shape[0])]
    df['post_shares'] = [post_shares for _ in range(df.shape[0])]
    df['post_description'] = [post_description for _ in range(df.shape[0])]
    df['date_scraped'] = [date_scraped for _ in range(df.shape[0])]


    df["Time"] = df["Time"].apply(harmonize_dates, args=[date_scraped]) #remove the "Il y a 3 jours" and change them to datetimes.
    #display(df["Time"])


    # à noter si besoin qu'il y a aussi les infos de 1- date de scraping 
    # et 2- date de publication (relativement à la date de scraping)

    return df


def harmonize_dates(comment_date, scraping_date):
    """We have a problem with the dataset: date of publication of some comments is sometimes "Published 5 days ago". This is not good for date analysis.
    We thus have this function that takes the scraping date and removes the accurate number of days to have a column with *only* datetimes.

    Args:
        df (pandas datagrame): the dataframe we want to harmonize.
    """


    if type(comment_date) == str:
        if comment_date[:2] == "Il": #si ça n'est pas un début de format datetime (en espérant que tous commencent ainsi)

            if comment_date[-1] in ["h", "n", "s"]: #n pour "min" mais je n'ai pas testé.
                return scraping_date #same date as scraping, just today.

            elif comment_date[-1] == "j": 
                nb_de_jours = int(comment_date[7]) #only one element bcz it should only be less than 10 days otherwise I guess (but haven't verified) that it would display a date.
                return (scraping_date - timedelta(days=nb_de_jours) )

            elif comment_date[-3:] == "sem": 
                nb_de_jours = 7 * int(comment_date[7]) #only one element bcz it should only be less than 10 days otherwise I guess (but haven't verified) that it would display a date.
                return (scraping_date - timedelta(days=nb_de_jours) )

        else: #it's just the good datetime
            return datetime.strptime(comment_date, "%d-%m-%Y") #to datetime
    else:
        return comment_date #if it's already a datetime.
        #if there is an error it *should* mean that it is a datetime (TypeError: 'Timestamp' object is not subscriptable)



def concatTikTok(d1, d2):
    return pd.concat([d1,d2])

def concatAllTikTok(out, out_filename, *data): #concatenate all dataframes contained in data iterable.

    for i,df in enumerate(data):
        if i==0:
            df0=df #on garde le 1er df auquel on va ajouter tt le monde.
        else:
            df0 = concatTikTok(df0,df) #rajouter les df un à un - c moche mais ça fonctionnera pour notre cas.

    if out:
        df0.to_csv("results/" + out_filename)
        #df0.to_pickle("results/" + out_filename)

    return df0
    

def test_harmonize_dates(df): #check if there is no weird data after.

    for i,el in df.iterrows(): #check if no one left.
        comment_date, scraping_date = el["Time"], el["date_scraped"]

        try:
            if comment_date[:2] == "Il":
                print(f'Warning ! One comment is remaining with bad date format: {comment_date}')

        except:
            pass

def test_codes():
    out=False
    out_filename=""

    d1 = read_tiktok_excel("data/test_tiktok_fusion.xlsx")
    d2 = read_tiktok_excel("data//tiktok_comments/Comments_1731413583.514067.xlsx")
    d3 = read_tiktok_excel("data/test_tiktok_fusion.xlsx")

    test_harmonize_dates(d1)

    concatenated_dataset = concatTikTok(d1,d2)

    full_concatenation = concatAllTikTok(out, out_filename, d1,d2,d3)

    ## display(concatenated_dataset)
    ## display(full_concatenation) #2353 rows



if __name__ == "__main__":
    print('------------ TikTok FUSION: Launching Tests')
    test_codes()
    print('------------ Tests Complete')
###### Code pour fusionner deux fichiers excel renvoyés par la méthode de scrapping TikTok

import pandas as pd
import csv
from IPython.display import display


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

    df['post_url'] = [url for _ in range(df.shape[0])]
    df['shown_comments']= [nb_coms_shown for _ in range(df.shape[0])]
    df['scraped_comments']= [nb_com_scraped for _ in range(df.shape[0])]
    df['difference']= [diff for _ in range(df.shape[0])]
    df['publisher'] = [publisher for _ in range(df.shape[0])]
    df['post_likes'] = [post_likes for _ in range(df.shape[0])]
    df['post_shares'] = [post_shares for _ in range(df.shape[0])]
    df['post_description'] = [post_description for _ in range(df.shape[0])]
    

    # à noter si besoin qu'il y a aussi les infos de 1- date de scraping 
    # et 2- date de publication (relativement à la date de scraping)

    return df

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

    return df0
    

def test_codes():
    out=False
    out_filename=""

    d1 = read_tiktok_excel("data/test_tiktok_fusion.xlsx")
    d2 = read_tiktok_excel("data/test_tiktok_fusion.xlsx")
    d3 = read_tiktok_excel("data/test_tiktok_fusion.xlsx")

    concatenated_dataset = concatTikTok(d1,d2)

    full_concatenation = concatAllTikTok(out, out_filename, d1,d2,d3)

    #display(concatenated_dataset)
    #display(full_concatenation) #2353 rows



if __name__ == "__main__":
    print('------------ TikTok FUSION: Launching Tests')
    test_codes()
    print('------------ Tests Complete')
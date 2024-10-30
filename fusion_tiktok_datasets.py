###### Code pour fusionner deux fichiers excel renvoyés par la méthode de scrapping TikTok

import pandas as pd
from IPython.display import display

import os
print(os.getcwd())


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

    df_posturl = list(pd.read_excel(path, skiprows=[0], nrows=0))
    print(df_posturl)
    df_posturl = df_posturl[1]
    df['post_url'] = [df_posturl for _ in range(df.shape[0])] # add new column to df

    # à noter si besoin qu'il y a aussi les infos de 1- date de scraping 
    # et 2- date de publication (relativement à la date de scraping)

    return df

def concatTikTok(d1, d2):
    return pd.concat([d1,d2])
    

def test_codes():

    d1 = read_tiktok_excel("data/Comments_1729173430.39675.xlsx")
    d2 = read_tiktok_excel("data/Comments_1729173430.39675 copie.xlsx")

    concatenated_dataset = concatTikTok(d1,d2)

    #display(concatenated_dataset)


if __name__ == "__main__":
    test_codes()
import pandas as pd


def parse_tiktok_comments(filename):

    tiktok_dtypes ={
        'Comment Number (ID)':int,
        "Nickname": str,
        "User @": str,
        "Comment Text": str, #pas de date car date_parser s'en occupe déjà
        "Likes": str, #HAS TO BE CHANGED AFTERWARDS (21.5K cannot be an int but should be converted to integer for robustness).
        'Profile Picture URL': str,
        'Is 2nd Level Comment': str,
        'User Replied To': str,
        'Number of Replies': int,
        'post_url': str,
        'shown_comments': int,
        'scraped_comments': int,
        'difference': int,
        }

    format = "%Y-%m-%d" #avant c'était "%d-%m-%Y" mais mtn que j'ai mis le pré-traitement dans fusion_tiktok_dataset, non

    tiktok = pd.read_csv(filename, dtype = tiktok_dtypes)#, parse_dates=parse_columns, date_parser=date_parser)
    tiktok["Time"] = pd.to_datetime(tiktok["Time"], format = format)

    return tiktok


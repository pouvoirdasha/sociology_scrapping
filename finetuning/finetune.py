# Mirror of finetuning.ipynb to try and trouble shoot

from autotrain.params import TextClassificationParams
from autotrain.project import AutoTrainProject

def get_hf_token():
    data=[]
    with open('data/hf_token_and_username.txt', newline='') as file:
        username = file.readline()
        hf_token = file.readline()

    return username, hf_token #username, token

HF_USERNAME, HF_TOKEN = get_hf_token() # get token from https://huggingface.co/settings/token


print(HF_USERNAME, HF_TOKEN)

params = TextClassificationParams(
    model="cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual",
    data_path="data/", #"Lyreck/tiktok_brat_comments", # path to the dataset on huggingface hub
    text_column="text", # the column in the dataset that contains the text
    target_column="label", # the column in the dataset that contains the labels
    train_split="train",
    valid_split="validation",
    epochs=3,
    batch_size=8,
    max_seq_length=512,
    lr=1e-5,
    optimizer="adamw_torch",
    scheduler="linear",
    gradient_accumulation=1,
    #mixed_precision="fp16", #need graphic card for this (no mps available)
    project_name="test",
    log="tensorboard",
    push_to_hub=True,
    username=HF_USERNAME,
    token=HF_TOKEN,
)
# tip: you can use `?TextClassificationParams` to see the full list of allowed parameters


# this will train the model locally
project = AutoTrainProject(params=params, backend="local", process=True)
project.create()
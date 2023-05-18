import streamlit as st
import googleapiclient.discovery
import isodate
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode

    
from transformers import AutoModelForTokenClassification
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence
import evaluate
import time

from datasets import Dataset, DatasetDict
from datasets import load_dataset
import keras
import tensorflow as tf

from streamlit_metrics import metric, metric_row
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pickle
import gdown
#sns.set(style="darkgrid", color_codes=True)
st.set_page_config(layout="wide",)


st.title('Predict views :clapper:')

st.header('Views prediction based on youtube video title')

st.write(f""" You can use this to predict how many views you might get depending on the title of your video. The model used is a pretrained model 'distilbert-base-uncased'. Enter your video title and predict how much views you'd get! """)

model = pickle.load(open('model.pkl', 'rb'))
with open('pages/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)
    

#model = AutoModelForSequenceClassification.from_pretrained("model", use_auth_token=True)
#tokenizer = AutoTokenizer.from_pretrained("tokenizer")
trainer = Trainer(model=model)

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

def pipeline_prediction(text):
    df=pd.DataFrame({'text':[text]})
    dataset = Dataset.from_pandas(df,preserve_index=False) 
    tokenized_datasets = dataset.map(tokenize_function)
    raw_pred, _, _ = trainer.predict(tokenized_datasets) 
    return(raw_pred[0][0])

title_text = st.text_input("Please enter a title")

submit = st.button("Submit", key='01')

try:
    if submit:
        with st.spinner(text="In progress..."):
            time.sleep(5)
        st.success('Done!')
        
        result = pipeline_prediction(title_text)
        st.markdown(f""" ## Your youtube title: {title_text}
        \n ### The predicted views: {int(result)}  :busts_in_silhouette:""")
        
    else:
        if len(title_text) > 0:
            st.write("No title text has been entered ")
except:
    raise



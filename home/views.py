import io
from django.shortcuts import render,redirect
from django.http import HttpResponse
import tensorflow as tf
from contextlib import redirect_stdout


# Create your views here.

def home(request):
  return render(request, "index.html")


def test(request):
  if request.method == 'POST':
    fake_news_model = request.POST.get('model')
    news = request.POST.get('news')
    if fake_news_model == "LSTM":
      import tensorflow as tf
      import numpy as np
      import pandas as pd
      import matplotlib.pyplot as plt
      import seaborn as sns
      import nltk
      import re
      from wordcloud import WordCloud
      import tensorflow as tf
      from gensim.models import Word2Vec
      import gensim
      from tensorflow.keras.preprocessing.text import Tokenizer
      from tensorflow.keras.preprocessing.sequence import pad_sequences
      from tensorflow.keras.models import Sequential
      from tensorflow.keras.layers import Dense, Embedding, LSTM, Conv1D, MaxPool1D
      from sklearn.model_selection import train_test_split
      from sklearn.metrics import classification_report, accuracy_score
      import pickle

      # Load the model
      lstm_model = tf.keras.models.load_model('home/static/imporvedfake.keras')

      summary_str = io.StringIO()
      with redirect_stdout(summary_str):
        lstm_model.summary()
      
      # Load the tokenizer from the file
      with open('home/static/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        
      news = news.lower()
      news_list = [news]
      maxlen = 1000
      news_list= tokenizer.texts_to_sequences(news_list)
      news_list = pad_sequences(news_list,maxlen=maxlen)
      result = (lstm_model.predict(news_list)>=0.5).astype(int)
      print(result)
      print(fake_news_model)
      
      context = {'news':news,
                'result':result}
      return render(request, 'test.html', context)
    
    elif fake_news_model == "BERT":
      import numpy as np
      import pandas as pd
      import pycaret
      import transformers
      from transformers import AutoModel, BertTokenizerFast
      import matplotlib.pyplot as plt
      from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
      from sklearn.model_selection import train_test_split
      from sklearn.metrics import classification_report
      import torch
      import torch.nn as nn
      
      # Load BERT model and tokenizer via HuggingFace Transformers
      bert = AutoModel.from_pretrained('bert-base-uncased')
      tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
      
      class BERT_Arch(nn.Module):
        def __init__(self, bert):
          super(BERT_Arch, self).__init__()
          self.bert = bert
          self.dropout = nn.Dropout(0.1)            # dropout layer
          self.relu =  nn.ReLU()                    # relu activation function
          self.fc1 = nn.Linear(768,512)             # dense layer 1
          self.fc2 = nn.Linear(512,2)               # dense layer 2 (Output layer)
          self.softmax = nn.LogSoftmax(dim=1)       # softmax activation function
        def forward(self, sent_id, mask):           # define the forward pass
          cls_hs = self.bert(sent_id, attention_mask=mask)['pooler_output']
                                                    # pass the inputs to the model
          x = self.fc1(cls_hs)
          x = self.relu(x)
          x = self.dropout(x)
          x = self.fc2(x)                           # output layer
          x = self.softmax(x)                       # apply softmax activation
          return x

      model = BERT_Arch(bert)
          
      
      # load weights of best model
      path = 'home/static/BERT_model_weights.pt'
      model.load_state_dict(torch.load(path))
      
      # testing on user data
      news = request.POST.get('news')
      print(news)
      print(fake_news_model)
      
      user_news_text = [news]

      # tokenize and encode sequences in the test set
      MAX_LENGHT = 500
      tokens_unseen = tokenizer.batch_encode_plus(
          user_news_text,
          max_length = MAX_LENGHT,
          pad_to_max_length=True,
          truncation=True
      )

      user_news_text_seq = torch.tensor(tokens_unseen['input_ids'])
      user_news_text_mask = torch.tensor(tokens_unseen['attention_mask'])

      with torch.no_grad():
        preds = model(user_news_text_seq, user_news_text_mask)
        preds = preds.detach().cpu().numpy()

      preds = np.argmax(preds, axis = 1)
      print(preds)
      
      context = {'result':preds}
      
      
      return render(request,'test.html', context)
    
    elif fake_news_model == "SVM":
      pass
    
    elif fake_news_model == "Logistic Regression":
      pass
      
    
  else:     
    return render(request, "test.html" )
    




# def testbert(request):
#   if request.method == 'POST':
#     import numpy as np
#     import pandas as pd
#     import pycaret
#     import transformers
#     from transformers import AutoModel, BertTokenizerFast
#     import matplotlib.pyplot as plt
#     from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
#     from sklearn.model_selection import train_test_split
#     from sklearn.metrics import classification_report
#     import torch
#     import torch.nn as nn
    
#     # Load BERT model and tokenizer via HuggingFace Transformers
#     bert = AutoModel.from_pretrained('bert-base-uncased')
#     tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    
#     class BERT_Arch(nn.Module):
#       def __init__(self, bert):
#         super(BERT_Arch, self).__init__()
#         self.bert = bert
#         self.dropout = nn.Dropout(0.1)            # dropout layer
#         self.relu =  nn.ReLU()                    # relu activation function
#         self.fc1 = nn.Linear(768,512)             # dense layer 1
#         self.fc2 = nn.Linear(512,2)               # dense layer 2 (Output layer)
#         self.softmax = nn.LogSoftmax(dim=1)       # softmax activation function
#       def forward(self, sent_id, mask):           # define the forward pass
#         cls_hs = self.bert(sent_id, attention_mask=mask)['pooler_output']
#                                                   # pass the inputs to the model
#         x = self.fc1(cls_hs)
#         x = self.relu(x)
#         x = self.dropout(x)
#         x = self.fc2(x)                           # output layer
#         x = self.softmax(x)                       # apply softmax activation
#         return x

#     model = BERT_Arch(bert)
        
    
#     # load weights of best model
#     path = 'home/static/BERT_model_weights.pt'
#     model.load_state_dict(torch.load(path))
    
#     # testing on user data
#     news = request.POST.get('news')
#     print(news)
    
#     user_news_text = [news]

#     # tokenize and encode sequences in the test set
#     MAX_LENGHT = 500
#     tokens_unseen = tokenizer.batch_encode_plus(
#         user_news_text,
#         max_length = MAX_LENGHT,
#         pad_to_max_length=True,
#         truncation=True
#     )

#     user_news_text_seq = torch.tensor(tokens_unseen['input_ids'])
#     user_news_text_mask = torch.tensor(tokens_unseen['attention_mask'])

#     with torch.no_grad():
#       preds = model(user_news_text_seq, user_news_text_mask)
#       preds = preds.detach().cpu().numpy()

#     preds = np.argmax(preds, axis = 1)
#     print(preds)
    
#     context = {'result':preds}
    
    
#     return render(request,'test2.html', context)
#   else:
#     return render(request,'test2.html')
  
  
  
def about(request):
  return render(request,'about.html')
    

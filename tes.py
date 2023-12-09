#standard packages
import pandas as pd
import datetime

#google map
import googlemaps as gm

#nlp
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

google_key ='AIzaSyCrtOY2laLo6_DLwkik3IBkiwdYUROwXAA'
dir = 'NPI_initial.xlsx'


class task_2:
    def __init__(self,
                 google_key
                 ,dir):
        self.google_key = google_key
        self.doctors = gm.Client(key=self.google_key)
        self.dir = dir

    def data_set_prep(self):
      df = pd.read_excel('{}'.format(self.dir))
      df['NPI'] = df['NPI'].astype(str)
      df['text_1'] = df['Last Name'] + ' ' + df['First Name']  + ' ' + df['NPI'] + ' ' + 'MD'
      df['text_2'] = df['Last Name'] + ' ' + df['First Name']  + ' ' + 'MD'
      df['text_3'] = df['Last Name'] + ' ' + df['First Name']  + ' ' + df['NPI']
      df['text_4'] = df['Last Name'] + ' ' + df['First Name']  + ' ' + 'NPI' + ' ' + df['NPI']
      return df

    def initial_results(self):
      df = self.data_set_prep()
      #Get the all options of all doctors' names
      doctors = df.iloc[:, -4:].values.tolist()
      doctorss = []
      for sublist in doctors:
          doctorss.extend(sublist)

      dfs = []
      for doctor in doctorss:
        #if the names of the doctors are even searchable
        try:
              doctors = self.doctors
              results = doctors.places(doctor)
              place_id = results['results'][0]['place_id']

              try:
                  doctorss = doctors.place(place_id = place_id)
                  doctorss['result']['reviews']

                  doctorss_reviews = []
                  #loop for get the whole relevant information to create a series
                  for elem in range(len(doctorss['result']['reviews'])):
                      text = doctorss['result']['reviews'][elem]['text']
                      rating = doctorss['result']['reviews'][elem]['rating']
                      original_language = doctorss['result']['reviews'][elem]['original_language']
                      relative_time_description = doctorss['result']['reviews'][elem]['relative_time_description']
                      author_name = doctorss['result']['reviews'][elem]['author_name']
                      time = doctorss['result']['reviews'][elem]['time']

                      #create series
                      doctorss_reviews.append({'text': text
                                              ,'rating': rating
                                              ,'original_language': original_language
                                              ,'relative_time_description': relative_time_description
                                              ,'author_name':author_name
                                              ,'time':time
                                              ,'doctor name': doctor})

                  #convert to dataframe
                  doctorss_reviews = pd.DataFrame(doctorss_reviews)

                  #convert time to datetime
                  doctorss_reviews['time'] = pd.to_datetime(doctorss_reviews['time'], unit='s')
                  doctorss_reviews = doctorss_reviews.sort_values(by='time', ascending=False)

                  #sentiment analysis
                  sid = SentimentIntensityAnalyzer()
                  doctorss_reviews['sentiment_score'] = doctorss_reviews['text'].apply(lambda x: sid.polarity_scores(x)['compound'])

                  dfs.append(doctorss_reviews)
              except:
                  print(f"There is no reviews for {doctor}")
        except:
            print(f"There is no such name as {doctor}")

      dfs = pd.concat(dfs, ignore_index=True)
      dfs = dfs.drop_duplicates(subset='text', keep='first').sort_values(by='sentiment_score', ascending=False).reset_index(drop=True)
      print(dfs)
      return dfs
    
Task_2 = task_2(google_key , dir)
Task_2.initial_results()
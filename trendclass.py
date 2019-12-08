"""
pytrends library practice 2

Mainly focus on Object oriented programming
class object file

version : 0.1 
Author : Hailey Lee
"""

from pytrends.request import TrendReq

class trendclass():
    def __init__(self,timef, kwlist=None , keyword = None, df):
        #initialize the object with constructor
        self.timeFrame = timef
        self.keywordList= kwlist
        self.keyword =  keyword
        self.dataframe = df


    def get_trend(self):
        pytrends = TrendReq(hl='en-EN', tz=360)

        kw_list = self.keywordList
        timeframe = self.timeFrame
        df = self.dataframe

        pytrends.build_payload([self.keyword], cat=0, timeframe=timeframe, geo='', gprop='')

        df = pytrends.interest_over_time()
        self.dataframe = df

        return df

    def get_12MA(self):
        df = self.dataframe
        df['12MA'] = df[self.keyword].rolling(window=52, min_periods=0).mean()

        self.dataframe = df

        return df




    def functionsForAnyUse(self):
        print(self.timeFrame)
        print(self.keywordList)

        print("You can use classes to have variables of its own and "
              "you can use those variables to act in different way ")

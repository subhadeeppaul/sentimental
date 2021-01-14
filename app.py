import os
import sys
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import re, tweepy, csv , textblob
app = Flask(__name__)


@app.route('/')
def analyze():
    tweetText = []
    tweets = []

    def DownloadData(self):
        # authenticating
        consumerKey = '8960pswi0ALmad8bD27Bofh22'
        consumerSecret = 'hSFcDZUsfwSbn3eutUirambdqLK1dwMyZkL40BAuoYY4mcbLbE'
        accessToken = '934833577803616257-mVf5WjNVNfT2eWmQ4T46N2T2BDFZ1tV'
        accessTokenSecret = '5xQVESFc6kGaQSbtdhvew1WPi73Yne1a9lTi62oPrkKba'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search

        searchTerm = input("Enter Keyword/Tag to search about: ")

        NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(
            api.search, q=searchTerm, lang="en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        positive = 0
        negative = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:
            # Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            
            # adding reaction of how people are reacting to find average later
            if (analysis.sentiment.polarity == 0.0):
                neutral += 1

            elif (analysis.sentiment.polarity > 0.0 and analysis.sentiment.polarity <= 1.0):
                positive += 1

            elif (analysis.sentiment.polarity >= -1.0 and analysis.sentiment.polarity < 0):
                negative += 1

        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = round((positive/NoOfTerms) * 100, 2)

        negative = round((negative / NoOfTerms) * 100, 2)

        neutral = round((neutral / NoOfTerms) * 100, 2)

        

        user = int(input("Enter the biasness : "))
                    # printing out data

        print("How people are reacting on " + searchTerm +
                  " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")


        if (user == 1):

            if (positive >= negative and positive >= neutral):
                print("Positive")
            elif (negative >= positive and negative >= neutral):
                print("Negative")
            else:
                print("Neutral")

            print()

            print("Detailed Report: ")

            print(str(positive) + "% people thought it was positive")

            print(str(negative) + "% people thought it was negative")

            print(str(neutral) + "% people thought it was neutral")
        elif(user == 0):
            if (positive >= negative and positive >= neutral):
                print("Negative")
            elif (negative >= positive and negative >= neutral):
                print("positive")
            else:
                print("Neutral")

            print("Detailed Report: ")

            print(str(negative) + "% people thought it was positive")

            print(str(positive) + "% people thought it was negative")

            print(str(neutral) + "% people thought it was neutral")           

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())


    return jsonify()


if (__name__ == "__main__"):
    app.run(debug=True)

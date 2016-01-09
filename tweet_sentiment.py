import sys
import json
#TODO: Log the tweets' text and the sentiment result to see if those are valid
import logging
def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))
def create_score_dict(in_file):
     # Creating a dictionary that contains all the words and scores
    afinnfile = in_file
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    return scores

def create_list_of_tweets(in_file):
    #Creating a list with the tweets
    tweets = []
    for line in in_file:
        tweets.append(json.loads(line))
    return tweets

#This method is used to calculate the score of a tweet
def calculate_tweet_score(scores,tweets):
    #Now, proceed to analyze the sentiment score of each tweet
    tweet_score_list = []
    tweet_count = 0
    for tweet in tweets:
        #If we're dealing with a deletion, the text can be ignored
        if tweet.keys()[0] == 'delete':
            continue
        else:
            current_score = 0
            unknown_temp = []
            #look for the word in the sentiment dictionary
            for word in tweet['text'].split():
                #If the word is there, add its score to the tweet, else do nothing
                if word in scores.keys():
                    current_score += scores[word]
                else:
                    current_score += 0
            #Add the score to the current list of scores
            tweet_score_list.append(current_score)
            tweet_count += 1 #And increment the index pointer
    return tweet_score_list



def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    #Creating a list with the sentiment scores
    scores = create_score_dict(sent_file)
    tweets = create_list_of_tweets(tweet_file)

    #Now, proceed to analyze the sentiment score of each tweet
    tweet_score_list = calculate_tweet_score(scores,tweets)
    for score in tweet_score_list:
        if score != None:
            print(score)
        else:
            print 0


if __name__ == '__main__':
    main()

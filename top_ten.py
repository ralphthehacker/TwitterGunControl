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

#Returns the top 10 hashtags
def top_10_hashtags(tweets):
    # Creating a dictionary to store the hashtags
    hashtag_dict = {}
    for tweet in tweets:
        if tweet.keys()[0] != 'delete':
            #Check if the tweet has any hashtags recorded onto it
            if tweet['entities'] is not None and (tweet['entities']['hashtags'] is not None):
                list_of_hashtags = tweet['entities']['hashtags']
                if len(list_of_hashtags) == 0:
                    continue
                else:
                    #Add all hashtags to the dictionary
                    for hashtag in list_of_hashtags:
                        if hashtag in hashtag_dict.keys():
                            hashtag_dict[hashtag['text']] = hashtag_dict[hashtag['text']] + 1
                        else:
                            hashtag_dict[hashtag['text']] = 1

    #Now return the top 10 hashtags
    sorted_dict = sorted(hashtag_dict,key=hashtag_dict.get)
    if len(sorted_dict)>=10:
        return (sorted_dict[len(sorted_dict):len(sorted_dict)-11:-1],hashtag_dict)
    else:
        return (sorted_dict, hashtag_dict)


def main():
    tweet_file = open(sys.argv[1])

    #Creating a list with the sentiment scores
    tweets = create_list_of_tweets(tweet_file)

    #Now, proceed to analyze the sentiment score of each tweet
    top_hashtags,hashtag_dict = top_10_hashtags(tweets)
    for hashtag in top_hashtags:
        print hashtag, hashtag_dict[hashtag]

if __name__ == '__main__':
    main()

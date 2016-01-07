import sys
import json

def create_list_of_tweets(in_file):
    #Creating a list with the tweets
    tweets = []
    for line in in_file:
        tweets.append(json.loads(line))
    return tweets

def calculate_term_frequency(tweets):
    #Create a dictionary containing the (word,count) pairs
    count_dict = {}
    total_count = 0
    #Iterate through every word in the tweets and count them
    for tweet in tweets:
        if tweet.keys()[0] != 'delete':
            for word in tweet['text']:
                # If the word isn't a user handle and it has been counted before, increment the count
                if word in count_dict.keys() and word[0] != '@' and word[0:1] != '\u':
                    count_dict[word] = (word,count_dict[word][1]+1)
                # Else, add it to the dictionary
                elif word[0] != '@' and word[0] != '\ ':
                    count_dict[word] = (word,1)
                # And increment the count of all the words in the dataset
                total_count+=1
    #After processing the file, just calculate the frequencies for each word
    for key in count_dict.keys():
        count_dict[key] = (key, float(count_dict[key][1])/total_count)
    return count_dict
def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    tweet_file = open(sys.argv[1])
     #Creating a list with the sentiment scores
    tweets = create_list_of_tweets(tweet_file)
    #Calculate the frequency of every term in the file
    frequency = calculate_term_frequency(tweets)

    print frequency
    lines(tweet_file)

if __name__ == '__main__':
    main()

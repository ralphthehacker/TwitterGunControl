import sys
import json

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

def calculate_tweet_score(scores,tweets):
    #Now, proceed to analyze the sentiment score of each tweet
    tweet_score_list = []
    tweet_count = 0
    for tweet in tweets:
        #If we're dealing with a deletion, the text can be ignored
        if tweet.keys()[0] == 'delete':
            tweet_score_list.append(0)
            tweet_count+=1
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



# This method finds the words that don't have a sentiment score and estimates them
# todo: The sentiment score is estimated by taking the average sentiment of all the tweets in which this word appears
def count_ratingless_scores(sent_scores, tweets,tweets_scores):

    #Initializing a dictionary that contains all words
    ratingless_words = {}     #todo: Key = word, Value = (sum_of_sentiments, number_of_ocurrences)

    #For every tweet, see if there are any ratingless words
    for index,tweet in enumerate(tweets):
        if tweet.keys()[0] != 'delete':
            # iterate word by word until you find something that's not in the sentiment dictionary
            for word in tweet['text'].split() :
                #Create a list to keep track of ratingless words that appeared in this tweet so that their scores are not exagg.
                seen_words = []
                if word not in sent_scores.keys():
                    #Two scenarios: Either the word has already been seen
                    if word in ratingless_words.keys():
                        # If this is the first time the word appears in a tweet, increase its score
                        cur_score = ratingless_words['word'][0]
                        cur_count = ratingless_words['word'][1]
                        if word not in seen_words:
                            ratingless_words['word'] = ( cur_score + tweets_scores[index],cur_count)
                            seen_words.append('word') #and flag the word as seen
                        # Then increase the count of ocurrences
                        ratingless_words['word'] = (cur_score,cur_count+1)
                    #or the word is completely new
                    else:
                        # If so, set it's base value to the tweet's sentiment score and default it to 1 ocurrence
                        ratingless_words['word'] = (tweets_scores[index],1)
                        # And flag the word as seen
                        seen_words.append(word)

    #Finally, normalize the scores for the sentiment scores and return them as a list

    for key in ratingless_words.keys():
        # Eliminate the tuples in the dictionary and substitute them by the score
        total_value = ratingless_words[key][0]
        ocurrences = ratingless_words[key][1]
        ratingless_words[key] = float(total_value)/float(ocurrences)

    return ratingless_words

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
     #Creating a list with the sentiment scores
    scores = create_score_dict(sent_file)
    tweets = create_list_of_tweets(tweet_file)

    #Calculating every tweet's sentiment score
    tweet_score_list = calculate_tweet_score(scores,tweets)

    # Then, calculate the scores of the words that are not present in the dictionary
    ratingless_words_scores = count_ratingless_scores(scores,tweets,tweet_score_list)
    for key in ratingless_words_scores.keys():
        print key,ratingless_words_scores[key]

    lines(sent_file)
    lines(tweet_file)
    lines(sent_file)
    lines(tweet_file)

if __name__ == '__main__':
    main()

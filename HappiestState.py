import sys
import json
import logging
def create_dict_us_states():
     return {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
    }
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
    return tweet_score_list

def determine_happiest_state(tweets,tweet_score_list,us_states):
    state_count = {}
    #For every tweet, print out its 'places' component
    for state_name in us_states.values():
        state_count[state_name] = 0

    for tweet in tweets:
        if tweet.keys()[0] != 'delete':
            for state_name in us_states.values():
                if state_name in tweet['place']['full_name']:
                    state_count[state_name]  =  state_count[state_name] + 1

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    #Creating a list with the sentiment scores
    scores = create_score_dict(sent_file)
    tweets = create_list_of_tweets(tweet_file)
    us_states = create_dict_us_states()

    #Now, proceed to analyze the sentiment score of each tweet
    tweet_score_list = calculate_tweet_score(scores,tweets)

    #Now, let's determine which state is the happiest
    determine_happiest_state(tweets,tweet_score_list,us_states)

    lines(sent_file)
    lines(tweet_file)

if __name__ == '__main__':
    main()

from app.home.imports import *
from run import app

def getTokenPrice(pair_id):
    headers = {
        'x-api-key': 'da2-vkmqkh3wlngdfktfeybq6j44li',
    }
    json_data = {
        'operationName': 'GetPairMetadata',
        'variables': {
            'pairId': pair_id,
        },
        'query': 'query GetPairMetadata($pairId: String!) {\n  pairMetadata(pairId: $pairId) {\n    price\n    exchangeId\n    fee\n    id\n    liquidity\n    liquidityToken\n    nonLiquidityToken\n    pairAddress\n    priceChange\n    priceChange1\n    priceChange12\n    priceChange24\n    priceChange4\n    tickSpacing\n    volume\n    volume1\n    volume12\n    volume24\n    volume4\n    token0 {\n      address\n      decimals\n      name\n      networkId\n      pooled\n      price\n      symbol\n      __typename\n    }\n    token1 {\n      address\n      decimals\n      name\n      networkId\n      pooled\n      price\n      symbol\n      __typename\n    }\n    __typename\n  }\n}\n',
    }
    response = requests.post('https://i3zwhsu375dqllo5srv5vn35ba.appsync-api.us-west-2.amazonaws.com/graphql',
                             headers=headers, json=json_data)
    return response.json()


def daySinceTweeted(created_at):

    # datetimed = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')

    data1 = created_at
    data2 = datetime.now()

    diff = data2 - data1

    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    has_day_passed = True if days >= 1 else False

    return has_day_passed
    

def getBarVariables(tweeted_at, pair_id, bar_type, currency, internal_id):
    one_day_since_tweeted = tweeted_at + timedelta(days=1)
    tweeted_at_timestamp = getTimeStamp(tweeted_at) # from
    day_after_tweet_timestamp = getTimeStamp(one_day_since_tweeted) # to

    TESTING_FROM = tweeted_at - timedelta(days=1)
    TESTING_TO = tweeted_at
    FROM_TEST = getTimeStamp(TESTING_FROM)
    TO_TEST = getTimeStamp(TESTING_TO)

    return {
        'symbol': pair_id,
        'from': FROM_TEST,
        'to': TO_TEST,
        'resolution': bar_type,
        'currencyCode': currency,
        'internal_id': internal_id
    }

def convertPricesToDict(prices):
    new_dict = {}
    for price in prices:
        new_dict[price] = prices[price]
    return new_dict

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        result = ((abs(current - previous)) / previous) * 100
        return round(result, 2)
    except ZeroDivisionError:
        return 0

def getPriceChange( old_price, new_price):
    if new_price != 0:
        if old_price != 0:
            percent = (new_price - old_price) / old_price * 100
        else:
            percent = new_price * 100
    elif new_price == 0 and old_price != 0:
        return -100
    else:
        percent = - old_price * 100
    return round(percent, 2)

def adjustInfluencerStats(user_id, prices):
    influencer = Follower.query.filter(Follower.user_id==user_id).first()

    ### This code sucks --- if the user has never tweeted a token and had the change data captured before, we hard code how to handle that case ###
    if influencer.tokens_tweeted == None:
        return setFirstStat(user_id, prices)

    original_price = prices["0"]

    h_performance =         getPriceChange( original_price, prices["1"])
    two_h_performance =     getPriceChange( original_price, prices["2"])
    three_h_performance =   getPriceChange( original_price, prices["3"])
    four_h_performance =    getPriceChange( original_price, prices["4"])
    twelve_h_performance =  getPriceChange( original_price, prices["12"])
    day_performance =       getPriceChange( original_price, prices["24"])

    
    influencer.tokens_tweeted += 1
    influencer.average_h_performance =        round((influencer.average_h_performance + h_performance) / influencer.tokens_tweeted, 2)
    influencer.average_two_h_performance =    round((influencer.average_two_h_performance + two_h_performance) / influencer.tokens_tweeted, 2)
    influencer.average_three_h_performance =  round((influencer.average_three_h_performance + three_h_performance) / influencer.tokens_tweeted, 2)
    influencer.average_four_h_performance =   round((influencer.average_four_h_performance + four_h_performance) / influencer.tokens_tweeted, 2)
    influencer.average_twelve_h_performance = round((influencer.average_twelve_h_performance + twelve_h_performance) / influencer.tokens_tweeted, 2)
    influencer.average_day_performance =      round((influencer.average_day_performance + day_performance) / influencer.tokens_tweeted, 2)

def setFirstStat(user_id, prices):
    influencer = Follower.query.filter(Follower.user_id==user_id).first()
    influencer.tokens_tweeted = 1
    original_price = prices["0"]
    influencer.average_h_performance =         getPriceChange( original_price, prices["1"])
    influencer.average_two_h_performance =     getPriceChange( original_price, prices["2"])
    influencer.average_three_h_performance =   getPriceChange( original_price, prices["3"])
    influencer.average_four_h_performance =    getPriceChange( original_price, prices["4"])
    influencer.average_twelve_h_performance =  getPriceChange( original_price, prices["12"])
    influencer.average_day_performance =       getPriceChange( original_price, prices["24"])


def update_influencers():
    print("UPDATING INFLUENCERS")

    with app.app_context():
        influencers = {}
        influencers_followed = Follower.query.filter(Follower.following==True)
        for influencer in influencers_followed:
            influencer_id = influencer.user_id
            influencers[influencer_id] = influencer

        ### >>> GET INFLUENCER DATA <<< ###
        API_KEY = 'zC4jO7rwJKgpSEk1Gea0Gn2UA'
        API_SECRET = 'W6GznkKdvmQJcW0SKu4SyuQ8oc3RIeopAnyrQKqfkJKMJkXo8s'
        ACCESS_TOKEN = '813561826629730304-blDojTpFwVvANOwv0GZwQiWQvHQXJ7s'
        ACCESS_TOKEN_SECRET = 'FEce0d2fGuty28hL81PssYmHqpLXrgx9EyquDpdbxi6Im'

        # Variables that contains the user credentials to access Twitter API 
        access_token = ACCESS_TOKEN
        access_token_secret = ACCESS_TOKEN_SECRET
        consumer_key = API_KEY
        consumer_secret = API_SECRET

        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        for influencer_id in influencers:
            new_user_data = api.get_user(user_id=influencer_id)
            # influencer = Follower.query.filter(Follower.user_id==id).first()
            influencer = influencers[influencer_id]
            influencer.follower_count = new_user_data.followers_count
        
        db.session.commit()


def scheduleTask():
    try:
        with app.app_context():
            tweets_to_collect = Tweet.query.filter(Tweet.token_price_collection_complete==False).all()
            
            information_to_collect = []
            tweets_to_update = []

            for tweet in tweets_to_collect:
                internal_id = tweet.id
                pair_id = tweet.pair_id
                tweeted_at = tweet.datetime
                bar_type = "1"
                currency = "USD"
                has_day_passed = daySinceTweeted(tweeted_at)
                if has_day_passed == False:
                    bar_variables = getBarVariables(tweeted_at, pair_id, bar_type, currency, internal_id)
                    information_to_collect.append(bar_variables)
                    tweets_to_update.append(tweet)

            if len(information_to_collect) > 0:
                GET_PRICE_BARS_LAMBDA_URL = "https://kmlkbz2ezqvfujkgvuknwg3pqq0zcvgy.lambda-url.us-west-2.on.aws/"
                payload = json.dumps({
                    "tokens": information_to_collect,
                    "authorization": "1c9052e6-1eg4-4d68-98a2-2bff5f2ec095"
                })
                headers = {
                    'Content-Type': 'text/plain'
                }
                response = requests.request("POST", GET_PRICE_BARS_LAMBDA_URL, headers=headers, data=payload)
                token_details = json.loads(response.text)

                for tweet in tweets_to_update:
                    internal_id = str(tweet.id)
                    price_details = token_details[internal_id]

                    tweet.prices = price_details
                    tweet.token_price_collection_complete = True

                    adjustInfluencerStats(tweet.user_id, price_details)

                    print('\nDetails for ' + internal_id)
                    print("")
                    print(price_details)
                    print('\n')
                
                db.session.commit()
            else:
                print("No tokens to collect price histories on for this interval check.")

    except Exception as e:
        print(e)
        do_nothing = True
        # Exception occurs before db is initialized on deployment ONLY.


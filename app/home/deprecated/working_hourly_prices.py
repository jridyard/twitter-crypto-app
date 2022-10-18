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

def hoursSinceTweeted(created_at):

    # datetimed = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')

    data1 = created_at
    data2 = datetime.now()

    diff = data2 - data1

    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return str(minutes) # can change to minutes for testing! :)

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

def scheduleTask():
    try:
        with app.app_context():
            tweets_to_collect = Tweet.query.filter(Tweet.token_price_collection_complete==False).all()

            for tweet in tweets_to_collect:
                token = tweet.token
                pair_id = tweet.pair_id
                token_prices = convertPricesToDict(tweet.prices)

                print("---token prices---")
                print(token_prices)
                print("---token prices---")

                tweeted_at = tweet.datetime
                hours_since_tweeted = hoursSinceTweeted(tweeted_at)
                print(hours_since_tweeted)

                if token_prices[hours_since_tweeted] == None:
                    print("********** COLLECTING NEW PRICE POINT **********")
                    token_price = float(getTokenPrice(pair_id)['data']['pairMetadata']['price'])
                    token_prices[hours_since_tweeted] = token_price
                    tweet.prices = token_prices

                    if hours_since_tweeted == '1':
                        change_percent = get_change(token_price, token_prices['0'])
                        tweet.priceChange1 = change_percent
                    
                    if hours_since_tweeted == '4':
                        change_percent = get_change(token_price, token_prices['0'])
                        tweet.priceChange4 = change_percent
                    
                    if hours_since_tweeted == '12':
                        change_percent = get_change(token_price, token_prices['0'])
                        tweet.priceChange12 = change_percent
                    
                    if hours_since_tweeted == '24':
                        change_percent = get_change(token_price, token_prices['0'])
                        tweet.priceChange24 = change_percent
                        tweet.token_price_collection_complete = True
            
            db.session.commit()
    except:
        do_nothing = True
        # Exception occurs before db is initialized on deployment ONLY.
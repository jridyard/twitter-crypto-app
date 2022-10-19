from app.base.models import *

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
    
    influencer.average_h_performance =        round(( (influencer.average_h_performance * influencer.tokens_tweeted) + h_performance) / (influencer.tokens_tweeted + 1), 2)
    influencer.average_two_h_performance =    round(( (influencer.average_two_h_performance * influencer.tokens_tweeted) + two_h_performance) / (influencer.tokens_tweeted + 1), 2)
    influencer.average_three_h_performance =  round(( (influencer.average_three_h_performance * influencer.tokens_tweeted) + three_h_performance) / (influencer.tokens_tweeted + 1), 2)
    influencer.average_four_h_performance =   round(( (influencer.average_four_h_performance * influencer.tokens_tweeted) + four_h_performance) / (influencer.tokens_tweeted + 1), 2)
    influencer.average_twelve_h_performance = round(( (influencer.average_twelve_h_performance * influencer.tokens_tweeted) + twelve_h_performance) / (influencer.tokens_tweeted + 1), 2)
    influencer.average_day_performance =      round(( (influencer.average_day_performance * influencer.tokens_tweeted) + day_performance) / (influencer.tokens_tweeted + 1), 2)

    influencer.tokens_tweeted += 1


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
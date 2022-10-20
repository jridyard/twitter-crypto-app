from app.home.imports import *

# Generic Routing Code \\//
@blueprint.route('/<template>')
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        # Detect the current page
        segment = get_segment(request)
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except:
        return render_template('home/page-500.html'), 500
# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
# (END) Generic Routing Code //\\

@blueprint.route('/index')
@login_required
def index():
    return redirect(url_for('home.home'))

@blueprint.route('/')
@login_required
def home():
    return render_template('home/index.html', segment='index')

@blueprint.route('/influencers')
@login_required
def influencers():
    return render_template('crypto/influencers.html', segment='influencers')

@blueprint.route('/tweets')
@login_required
def tweets():
    already_created = NewTweetCheck.query.filter(NewTweetCheck.id==1).first()
    if already_created != None:
        already_created.new_tweet = "False"
        db.session.commit()

    return render_template('crypto/tweets.html', segment='tweets')


### GET FOLLOWERS ###
@blueprint.route('/api/get_followers', methods=["GET", "POST"])
@cross_origin()
def get_followers():
    
    followers =  Follower.query.filter(Follower.following==True).all()
    follower_list = []
    for follower in followers:
        follower_list.append({
            'name': follower.name,
            'user_id': follower.user_id,
            'follower_count': follower.follower_count,
            'screen_name': follower.screen_name,
            'tokens_tweeted': follower.tokens_tweeted,
            'performance': {
                "1": follower.average_h_performance,
                "2": follower.average_two_h_performance,
                "3": follower.average_three_h_performance,
                "4": follower.average_four_h_performance,
                "12": follower.average_twelve_h_performance,
                "24": follower.average_day_performance
            }
        })

    return make_response(jsonify({
        'follower_list': follower_list
    }), 200)






### GET TWEETS AWAITING TOKEN PRICE DATA ###
@blueprint.route('/api/tokens_awaiting_price_data', methods=["GET", "POST"])
@cross_origin()
def tokens_awaiting_price_data():
    tweets = Tweet.query.filter(Tweet.token_price_collection_complete==False)
    result = schemaToJSON(TweetSchema(), tweets)
    return make_response(jsonify(result), 200)

### GET TWEETS AWAITING TOKEN PRICE DATA ###
@blueprint.route('/api/update_prices', methods=["GET", "POST"])
@cross_origin()
def update_prices():
    json = request.get_json()['data_to_update']

    mappings_to_update = []
    for key in json:
        id = key
        prices = json[key]
        mappings_to_update.append({
            'token_price_collection_complete': True,
            'prices': prices,
            'id': int(id)
        })
        
    db.session.bulk_update_mappings(Tweet, mappings_to_update)
    db.session.commit()
    return make_response(jsonify({
        'response': 'ok'
    }), 200)

# TODO: add bulk updatemappings call for updating each influencers avg performance stats
# implement the endpoint in the twc_stream directory or w/e
# ... then do the same thing for updating the once per 24h influencer update stuff


### UPDATE INFLUENCER STATS ###
@blueprint.route('/api/update_influencer_stats', methods=["GET", "POST"])
@cross_origin()
def update_influencer_stats():
    details_to_update = request.get_json()['data_to_update']

    for details in details_to_update:
        user_id = details['user_id']
        prices = details['prices']

        adjustInfluencerStats(user_id, prices)

    db.session.commit()

    return make_response(jsonify({
        'response': 'ok'
    }), 200)

### UPDATE INFLUENCER STATS ###
@blueprint.route('/api/get_influencers', methods=["GET", "POST"])
@cross_origin()
def get_influencers():
    influencers = Follower.query.all()
    result = schemaToJSON(FollowerSchema(), influencers)
    return make_response(jsonify(result), 200)

@blueprint.route('/api/update_influencer_info', methods=["GET", "POST"])
@cross_origin()
def update_influencer_info():
    influencers = request.get_json()['data_to_update']

    mappings_to_update = []
    for influencer in influencers:
        user_id = influencer['user_id']
        follower_count = influencer['follower_count']
        mappings_to_update.append({
            'follower_count': follower_count,
            'user_id': str(user_id)
        })
        
    db.session.bulk_update_mappings(Follower, mappings_to_update)
    db.session.commit()
    return make_response(jsonify({
        'response': 'ok'
    }), 200)




### ADD INFLUENCERS ###
@blueprint.route('/api/add_influencer', methods=["GET", "POST"])
@cross_origin()
def add_influencer():
    data = request.get_json()
    influencer_handle = data['handle'].lower()

    influencer = Follower.query.filter_by(screen_name=str(influencer_handle)).first()
    if influencer:
        influencer.following = True
        db.session.commit()
        return make_response(jsonify({
            'ok': True,
            'follower_data': {
                'name': influencer.name,
                'follower_count': influencer.follower_count,
                'user_id': influencer.user_id,
                'screen_name': influencer.screen_name,
                'verified': influencer.verified
            }
        }))

    user = get_user_from_twitter_api(influencer_handle)
    ### >>> GET INFLUENCER DATA <<< ###

    # Save the new follower
    follower = Follower(
        name=user.name,
        follower_count=user.followers_count,
        user_id=user.id,
        screen_name=user.screen_name.lower(),
        verified=user.verified,
        following=True
    )

    db.session.add(follower)
    db.session.commit()

    return make_response(jsonify({
        'ok': True,
        'follower_data': {
            'name': user.name,
            'follower_count': user.followers_count,
            'user_id': user.id,
            'screen_name': user.screen_name.lower(),
            'verified': user.verified
        }
    }), 200)


### UNFOLLOW INFLUENCERS ###
@blueprint.route('/api/unfollow_influencer', methods=["GET", "POST"])
@cross_origin()
def unfollow_influencer():
    data = request.get_json()
    user_id = data['user_id']

    follower = Follower.query.filter_by(user_id=str(user_id)).first()
    if follower:
        follower.following = False
        db.session.commit()
        return make_response(jsonify({
            'ok': True
        }))

    return make_response(jsonify({
        'ok': False,
        'message': 'Influencer does not exist. Cannot unfollow since influencer not available in DB.'
    }))

@blueprint.route('/api/add_tweet', methods=["GET", "POST"])
@cross_origin()
def add_tweet():
    print('ADDING TWEET?')
    tweet_data = json.loads( request.get_json() )
    print(tweet_data)

    # screen_name = get_user_id_from_twitter_api(tweet_data['user_id']).screen_name.lower()
    screen_name = Follower.query.filter(Follower.user_id==str(tweet_data['user_id'])).first().screen_name

    # tweeted_at = datetime.strptime(tweet_data['created_at'], ).date()
    # print(tweet_data['created_at'])

    curr_price = float(tweet_data['price']) # FLOAT!

    tweet = Tweet(
        name=screen_name,
        user_id=tweet_data['user_id'],
        tweet=tweet_data['text'],
        datetime=datetime.utcnow(),
        token=tweet_data['token'], # token_id *thats what token actually is.
        price_at_tweet=tweet_data['price'],
        pair_id=tweet_data['pair_id'],
        token_name=tweet_data['token_name'],
        tweet_id = str(tweet_data['tweet_id']),
        token_price_collection_complete = False
    )

    db.session.add(tweet)
    db.session.commit()

    return make_response(jsonify({
        'response': 'Added tweet!'
    }), 200)


@blueprint.route('/api/get_tweets', methods=["GET", "POST"])
@cross_origin()
def get_tweets():

    tweets = Tweet.query.all()
    tweet_list = []
    for tweet in tweets:
        tweet_list.append({
            'name': tweet.name,
            'id': tweet.id,
            'tweet': tweet.tweet,
            'token_name': tweet.token_name,
            'token': tweet.token,
            'tweet_id': tweet.tweet_id,
            'datetime': tweet.datetime,
            'prices': {
                '0': tweet.prices['0'],
                '1': tweet.prices['1'],
                '2': tweet.prices['2'],
                '3': tweet.prices['3'],
                '4': tweet.prices['4'],
                '12': tweet.prices['12'],
                '24': tweet.prices['24'],
            }
        })
        

    return make_response(jsonify({
        'tweet_list': tweet_list
    }), 200)

@blueprint.route('/drop_tweets', methods=["GET", "POST"])
def drop_tweets():

    tweets = Tweet.query.all()
    for tweet in tweets:
        db.session.delete(tweet)

    db.session.commit()

    return "Success"


@blueprint.route('/api/check_tweets', methods=["GET", "POST"])
@cross_origin()
def check_tweets():
    already_created = NewTweetCheck.query.filter(NewTweetCheck.id==1).first()

    if already_created == None:
        return make_response(jsonify({
            'response': 'Nothing New'
        }), 200)

    if already_created.new_tweet == "True":
        already_created.new_tweet = "False"
        db.session.commit()
        return make_response(jsonify({
            'response': 'New Tweet',
            'data': already_created.tweet_data
        }), 200)

    return make_response(jsonify({'response': 'Nothing New'}), 200)

@blueprint.route('/api/post_new_tweets', methods=["GET", "POST"])
@cross_origin()
def post_new_tweets():

    tweet_data = json.loads( request.get_json() )

    # screen_name = get_user_id_from_twitter_api(tweet_data['user_id']).screen_name.lower()
    screen_name = Follower.query.filter(Follower.user_id==str(tweet_data['user_id'])).first().screen_name
    tweet_data['name'] = screen_name

    already_created = NewTweetCheck.query.filter(NewTweetCheck.id==1).first()
    if already_created == None:
        new_tweet = NewTweetCheck(id = 1, new_tweet = "True", tweet_data = tweet_data)
        db.session.add(new_tweet)
        db.session.commit()
    else:
        already_created.new_tweet = "True"
        already_created.tweet_data = tweet_data
        db.session.commit()

    return make_response(jsonify({
        'response': 'Success'
    }), 200)
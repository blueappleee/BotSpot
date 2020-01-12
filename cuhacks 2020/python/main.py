# gets relevant information about a twitter user for determining if a bot

# import modules
import twitter
import creds
import string
import statistics
from flask import Flask, request
import pickle
from sklearn import tree, metrics
import pandas as pd

app = Flask(__name__)

# checks if bot is in check as a seperate word from any other words. ex bottom does not count but bot_tom would. if 1 then bot is in, if 0 then bot isnt
def instring(check):
    for i in range(len(check)):
        character = check[i].lower()
        if character == 'b':
            if i != 0:
                if (ord(check[i - 1].lower()) < 97 or ord(check[i - 1].lower()) > 122):
                    if (len(check) > i + 1) and (check[i + 1].lower() == 'o' or check[i + 1].lower() == '0'):
                        if (len(check) > i + 2) and check[i + 2].lower() == 't':
                            if (len(check) > i + 3) and (ord(check[i + 3].lower()) < 97 or ord(check[i + 3].lower()) > 122):
                                return 1

                            elif ((len(check) == i + 3)):
                                return 1

            else:
                if (len(check) > i + 1) and (check[i + 1].lower() == 'o' or check[i + 1].lower() == '0'):
                    if (len(check) > i + 2) and check[i + 2].lower() == 't':
                        if (len(check) > i + 3) and (ord(check[i + 3].lower()) < 97 or ord(check[i + 3].lower()) > 122):
                            return 1

                        elif ((len(check) == i + 3)):
                           return 1

    return 0
                        
        

# grabs the user whos name is provided information
@app.route('/', methods = ["GET", "POST"])
def usertweet():

    if request.method == 'POST':
        name = request.form.get("name")
    else:
        name = request.args.get("name")
    #Twitter API credentials
    consumer_key = creds.creds[0]
    consumer_secret = creds.creds[1]
    access_key = creds.creds[2]
    access_secret = creds.creds[3]

    api = twitter.Api(consumer_key= consumer_key,
                  consumer_secret= consumer_secret,
                  access_token_key= access_key,
                  access_token_secret= access_secret)

    # grab the users data
    try:
        results = api.GetUser(screen_name = name, return_json = True)

    # if user doesnt exist return empty list
    except twitter.error.TwitterError:
        return []

    for attribute in results:
        attribute.encode('unicode-escape').decode('utf-8')

    #gets rid of emojis in name or description
    printable = set(string.printable)

    results["screen_name"] = ''.join(filter(lambda x: x in printable, results["screen_name"]))
    results["description"] = ''.join(filter(lambda x: x in printable, results["description"]))

    # list of relevent data parameters
    data = [#results["screen_name"],
            #results["description"],
            #results["name"],
            results["followers_count"],
            results["friends_count"],
            results["listed_count"],
            results["favourites_count"],
            results["statuses_count"],
            results["verified"],
            #results["created_at"],
            #results["id"]
            ]
    
    data = pd.DataFrame(data)
    
    # checks if bot is in name
    namedesc = instring(results["screen_name"])

    # if bot isnt in name then check the description
    if namedesc == 0:
        namedesc = instring(results["description"])

    # if namedesc == 1 then user has bot in their description or name
    #data.append(namedesc)

    tweets = api.GetUserTimeline(screen_name = name)

    times = []

    # add time of each tweet to a list
    for tweet in tweets:
        times.append(tweet.created_at_in_seconds)

    # calculate stdev between each tweet time
    stdev = statistics.stdev(times)

    #data.append(stdev)
    
    loaded_model = pickle.load(open("finalized_model.sav", 'rb'))
    result = loaded_model.predict(data.values.reshape(1,-1))

    # return the data
    return str(result)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

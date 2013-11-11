#!/usr/bin/python

import twython, time, pprint, traceback
from twython import TwythonStreamer

APP_KEY=""
APP_SECRET=""
OAUTH_TOKEN=""
OAUTH_SECRET=""
MAXPERHOUR=4
OVERALLMAXPERHOUR=50

lasttry=0

class MyStreamer(TwythonStreamer):
    friends = []
    rts = []
    twitter = None
    def update_friends(self, friendlist):
        self.friends = friendlist
        print("updated friends", self.friends)
    def cleanrts(self):
        for r in self.rts:
            u,i,m,t = r
            if t < time.time() - 3600:
                self.rts.remove(r)
    def rt(self, user, userid, tweet):
        self.cleanrts()
        if self.twitter is not None:
            if not tweet in [ m for u,i,m,t in self.rts ]:
                if userid in self.friends or len([ u for u,i,m,t in self.rts if u == user]) < MAXPERHOUR:
                    if len(self.rts) < OVERALLMAXPERHOUR:
                        print("retweeting %s (%d): %s" % (user, userid, tweet))
                        msg = ("RT @%s: %s" % (user, tweet[len(self.creds['screen_name'])+1:].lstrip(': ')))[0:138]
                        twitter.update_status(status=msg.encode('utf-8'))
                        self.rts.append( (user, userid, tweet, time.time(), ) )
                    else:
                        print("Overall rate limit exceeded")
                else:
                    print("Rate limit exceeded", user)
            else:
                print("Tweet has been posted already: ", user, tweet)
    def tweet(self, tweet):
        if self.twitter is not None:
            twitter.update_status(status=tweet[0:140])
    def on_success(self, data):
        if 'text' in data:
            print ("%s: %s" % (data['user']['screen_name'], data['text'])).encode('utf-8')
            #print data
            if data['text'].lower().startswith("@%s" % self.creds['screen_name'].lower()):
                self.rt(data['user']['screen_name'], data['user']['id'], data['text'])
        elif 'direct_message' in data:
            print ("DM %s: %s" % (data['direct_message']['sender']['screen_name'], data['direct_message']['text']))
            self.tweet(data['direct_message']['text'])
        elif 'friends' in data:
            self.update_friends(data['friends'])
        else:
            print("unknown notification received")

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()

while True:
    try:
        twitter = twython.Twython(app_key=APP_KEY, app_secret=APP_SECRET, oauth_token=OAUTH_TOKEN, oauth_token_secret=OAUTH_SECRET)
        creds = twitter.verify_credentials()
        userid = creds['id_str']

        stream = MyStreamer(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_SECRET)
        stream.twitter = twitter
        stream.creds = creds

        stream.user()
    except Exception, e:
        print('==Exception==')
        print(e)
        print(traceback.format_exc())
        if int(time.time()) - lasttry < 120:
            print('==Too many Exceptions in the last 2 minutes, exiting...')
            break
        else:
            time.sleep(5)
            lasttry = int(time.time())


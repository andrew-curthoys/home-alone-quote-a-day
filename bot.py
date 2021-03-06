from quotes import quotes
from utils import get_auth, txgvg_dt
import requests
from datetime import datetime
import time

class Tweeter:
    def __init__(self):
        self.auth = get_auth()
        self.start_date = datetime.strptime('2020-11-27', '%Y-%m-%d')

    def send_tweet(self):
        # Get quote ID based on date since Black Friday
        quote_id = (datetime.now() - self.start_date).days

        status_update_endpoint = 'https://api.twitter.com/1.1/statuses/update.json'

        if quote_id == 19:
            full_quote = quotes[quote_id]
            tweet1 = full_quote[:188]
            tweet2 = quotes[quote_id][188:len(full_quote)-30]
            tweet3 = full_quote[len(full_quote)-30:]
            data1 = {'status': tweet1}
            tweet1_obj = requests.post(status_update_endpoint, auth=self.auth, data=data1)
            tweet1_id = tweet1_obj.json()['id_str']
            data2 = {'status': tweet2, 'in_reply_to_status_id': tweet1_id}
            tweet2_obj = requests.post(status_update_endpoint, auth=self.auth, data=data2)
            tweet2_id = tweet2_obj.json()['id_str']
            data3 = {'status': tweet3, 'in_reply_to_status_id': tweet2_id}
            requests.post(status_update_endpoint, auth=self.auth, data=data3)

        else:
            tweet = quotes[quote_id]
            data = {'status': tweet}
            requests.post(status_update_endpoint, auth=self.auth, data=data)

    def delete_tweet(self, tweet_id):
        delete_endpoint_root = 'https://api.twitter.com/1.1/statuses/destroy/'
        delete_endpoint = delete_endpoint_root + tweet_id + '.json'
        requests.post(delete_endpoint, auth=self.auth)

    def get_tweet_timeline(self):
        home_timeline_endpoint = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
        home_timeline = requests.get(home_timeline_endpoint, auth=self.auth)
        return home_timeline.json()

    def delete_timeline(self):
        home_timeline = self.get_tweet_timeline()
        for tweet in home_timeline:
            tweet_id = tweet.get('id_str')
            self.delete_tweet(tweet_id)

def home_alone_season(dt: datetime):
    # Get date info
    dt_info = dt.timetuple()
    dt_month = dt_info.tm_mon
    dt_year = dt_info.tm_year
    
    # Get Thanksgiving date & set XMas variable
    first_of_nov = datetime(dt_year, 11, 1)
    first_of_nov_wday = first_of_nov.timetuple().tm_wday
    txgvg = datetime(dt_year, 11, txgvg_dt[first_of_nov_wday])
    xmas = datetime(dt_year, 12, 25)

    # Check if it's Home Alone season
    if dt > txgvg and dt <= xmas:
        return True
    else:
        return False


if __name__ == "__main__":
    dt = datetime.now()

    # Check if it's Home Alone Season baby
    if home_alone_season(dt):
        tweeter = Tweeter()
        tweeter.send_tweet()
    else:
        print("Oh no! It's not Home Alone season :(")

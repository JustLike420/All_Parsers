import os
import tweepy
from dotenv import load_dotenv

load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
USERNAME = os.getenv('USERNAME')


def get_user_following(username):
    all_users = []
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        wait_on_rate_limit=True)

    user = client.get_user(username=username)
    user_id = user.data.id
    paginator = tweepy.Paginator(client.get_users_following, user_id, max_results=1000)

    for response_page in paginator:
        for data in response_page.data:
            all_users.append(data.username)
    return all_users


if __name__ == '__main__':
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, SECRET_TOKEN)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    input_user_link = input('[+] Input user link: ')
    input_username = input_user_link.split('/')[-1]

    users = get_user_following(input_username)
    print(input_username, len(users))
    for user in users:

        user1 = api.get_friendship(source_screen_name=USERNAME, target_screen_name=user)

        if user1[0].can_dm:
            print(f'https://twitter.com/{user}')
            with open('results.txt', 'a', encoding='utf-8') as file:
                file.write(f'https://twitter.com/{user}\n')

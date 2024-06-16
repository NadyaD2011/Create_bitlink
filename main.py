from urllib.parse import urlparse
import requests
import os
from dotenv import load_dotenv


def shorten_link(api_token, long_url):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
      "Authorization": "Bearer {}".format(api_token)
    }
    payload = {'long_url' : long_url}
  
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    response_link = response.json()['link']
    return response_link


def count_clicks(api_token, bitlink):
    bitlink = urlparse(bitlink)
    click_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink.netloc}{bitlink.path}/clicks/summary'
    params = {
      'units' : -1,
      "unit": "day"
    }
    headers = {
      "Authorization": "Bearer {}".format(api_token)
    }
    
    response = requests.get(click_url, headers=headers, params=params)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(user_url, api_token):
    user_url = urlparse(user_url)
    bitlink_url =  f'https://api-ssl.bitly.com/v4/bitlinks/{user_url.netloc}{user_url.path}'
    headers = {
      "Authorization": "Bearer {}".format(api_token)
    }
    response = requests.get(bitlink_url, api_token, headers=headers)
    return response.ok


def main():
    load_dotenv()
    api_token = os.environ["BITLY_API_KEY"]
    parser = argparse.ArgumentParser()
    parser.add_argument("long_url", help="Вашу ссылку")
    args = parser.parse_args()
    long_url = args.long_url

    try:
        if is_bitlink(user_url=long_url, api_token=api_token):
            print("Здесь будет кликов на сыллку", count_clicks(api_token, long_url))
        else:
            print(shorten_link(api_token, long_url))
    except requests.exceptions.HTTPError as error:
        print("Can't get data from server:\n{0}".format(error))


if __name__ == '__main__':
    main()
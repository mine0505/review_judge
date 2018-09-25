import requests
import json
import pprint

search_api_url = 'https://itunes.apple.com/search'
review_api_url = 'https://itunes.apple.com/jp/rss/customerreviews/id={}/sortBy=mostRecent/json'

def search(word):
    params = {'term': word, 'media': 'movie', 'entity': 'movie', 'country': 'jp', 'lang': 'ja_jp', 'limit': '10'}
    r = requests.get(search_api_url, params=params)

    search_result = []
    if r.status_code == 200:
        json_data = r.json()
        #pprint.pprint(json_data, depth=3, compact=True)
        print(str(json_data['resultCount']) + ' 件のiTunes Store検索結果')

        for result in json_data['results']:
            search_result.append({'title': result['trackName'], 'id': result['trackId']})
            print('なまえ\t' + result['trackName'])
            print('ID\t' + str(result['trackId']))
            print('------------------------------')
        #print(search_result)

    return search_result

def get_review(movie_id):
    r = requests.get(review_api_url.format(movie_id))

    reviews = []
    if r.status_code == 200:
        json_data = r.json()

        for result in json_data['feed']['entry']:
            for k, v in result.items():
                if k == 'content':
                    reviews.append(v['label'])
        print(reviews)

    return reviews

'''
if __name__ == '__main__':
    search(input('検索ワードを入力:'))
    get_review(input('Type id:'))
'''
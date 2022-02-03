from flask import Flask, jsonify
import newspaper
import json

app = Flask(__name__)

newspapers = {  
    'zeit': 'http://zeit.de', 
    'tagesspiegel': 'https://www.tagesspiegel.de/'
}


def process_article(article):
    try:
        article.download()
        article.parse()
        return {
                'title': article.title,
                'url': article.url,
        }
    except: 
        pass
    
def process_newspaper(newspaper_url):
    articles = newspaper.build(newspaper_url).articles
    return [process_article(a) for a in articles]


### API

@app.route('/newsapi/<newspaper_id>')
def get_news_by_newspaper(newspaper_id):
    # show the user profile for that user
    return jsonify(news.get(newspaper_id, {}))

if __name__ == "__main__":
    port = 5001
    news = json.load(open('news.json'))
    app.run(host='0.0.0.0', port = port)


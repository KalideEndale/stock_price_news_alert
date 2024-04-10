import requests
import datetime
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "REDACTED"
STOCK_API_KEY = "REDACTED"

account_sid = "REDACTED"

auth_token = "REDACTED"

params = {
    "q": COMPANY_NAME or STOCK,
    "apiKey": NEWS_API_KEY,


}
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}


# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
current_close = datetime.date.today() - datetime.timedelta(days=1)
previous_close = current_close - datetime.timedelta(days=1)
print(current_close)
print(previous_close)

stock_update = requests.get(STOCK_ENDPOINT, stock_params)
stock_update.raise_for_status()
stock_closing = stock_update.json()
daily_reports = stock_closing["Time Series (Daily)"]
print(daily_reports)

current_day_close = float(daily_reports[str(current_close)]['4. close'])
previous_day_close = float(daily_reports[str(previous_close)]['4. close'])
print(previous_day_close)
difference = current_day_close - previous_day_close
pct_change = int((abs(difference) / previous_day_close) * 100)

#fetch the first 3 articles for the COMPANY_NAME.
news_update = requests.get(NEWS_ENDPOINT, params)
news_update.raise_for_status()
stock_news = news_update.json()
relevant_news_articles = stock_news['articles'][:3]


# Send a separate message with each article's title and description to your phone number.
article_titles = [article['title'] for article in relevant_news_articles]
article_desc = [article['description'] for article in relevant_news_articles]

#Format the SMS message
# if pct_change > 5:
if difference > 0:
    for index in range(len(article_titles)):
        "\n"
        client = Client(account_sid, auth_token)
        message = client.messages \
        .create(
            body =  f"{STOCK}: 🔺{round(pct_change,2)}% \n" \
                    f"Headline: {article_titles[index]} \n" \
                    f"Brief: {article_desc[index]}",
            from_ ='+1REDACTED',
            to = '+1REDACTED'
        )
else:
    for index in range(len(article_titles)):
        client = Client(account_sid=account_sid)
        message = client.messages \
        .create(
            body=f"{STOCK}: 🔻{round(pct_change, 2)}% \n" \
                 f"Headline: {article_titles[index]} \n" \
                 f"Brief: {article_desc[index]}",
            from_='+18335481061',
            to='+17577068125'
        )


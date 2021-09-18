import random
import tweepy
from datetime import date, timedelta
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# VARIABLES
consumer_key = 'KeraZURjJJWGmVHU7iDUh7Lyt'
consumer_secret = 'fCnF0sS9YI3GqZpzK4KvMjd9qiFLiDw21m7LqVuvSWlqxYrv7Z'

access_token = '1434826268378157056-x7c35ain34Oaez0xNey3GTIjpnirdN'
access_token_secret = 'SwWZ2zZtRwxLn3NX2GIiF3VqulXao6ziFypANGXmOXKPN'

FILE_NAME = 'SmallProjects/MARKETVISOR BOT/last_seen.txt'
RETWEET_LIST = 'SmallProjects/MARKETVISOR BOT/retweet_list.txt'

# STARTING THE API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# FUNCTIONS
def like_the_mentions():
    def read_last_seen(FILE_NAME):
        file_read = open(FILE_NAME, 'r')
        last_seen_id = int(file_read.read().strip())
        file_read.close()
        return last_seen_id

    def store_last_seen(FILE_NAME, id):
        file_write = open(FILE_NAME, 'w')
        file_write.write(str(id))
        file_write.close()
        return

    last_seen_id = read_last_seen(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
        if 'TheMARKETVISOR' or 'THE MARKETVISOR BOT' or 'THEMARKETVISORBOT' in mentions.full_text.lower():
            last_seen_id = mention.id
            store_last_seen(FILE_NAME, last_seen_id)
            print(str(mention.id) + " - " + mention.full_text)
            try:
                api.create_favorite(mention.id)
            except Exception as error:
                print(error)

            store_last_seen(FILE_NAME, mention.id)

    print("Liked all your posts, BOSS.")


def retweeting_market_news():
    def read_last_seen_retweet(RETWEET_LIST):
        file_read_retweet = open(RETWEET_LIST, 'r')
        last_seen_id_retweet = file_read_retweet.read().strip()
        file_read_retweet.close()
        return last_seen_id_retweet

    def store_last_seen_retweet(RETWEET_LIST, id):
        file_write_retweet = open(RETWEET_LIST, 'w')
        file_write_retweet.write(str(id))
        file_write_retweet.close()
        return

    last_retweet_id = read_last_seen_retweet(RETWEET_LIST)
    timeline_tweets = api.home_timeline(last_retweet_id)

    for tweets in timeline_tweets:
        last_retweet_id = tweets.id
        store_last_seen_retweet(RETWEET_LIST, last_retweet_id)
        print(f"{tweets.author.name} - {tweets.text}\n")
        print(tweets.id)
        try:
            api.retweet(tweets.id)
        except Exception as error:
            print(error)

        store_last_seen_retweet(FILE_NAME, tweets.id)
    print("Retweeted all the tweets from your time line, BOSS.")


def Virtual_games_recommendation():
    pass


def market_open_close_tweets():
    def opening_bell():
        tickers = ["^NSEI", "^BSESN"]
        date_today = date.today()

        data_today = yf.download(tickers, date_today)
        today_open = data_today["Open"]

        date_yest = date_today - timedelta(days=1)
        data_yest = yf.download(tickers, date_yest)
        yest_close = data_yest["Close"]
        yestclose_todayopen_diff = yest_close - today_open

        details = f"TODAY-OPEN: \n {today_open} \n YEST-CLOSE--TODAY-OPEN-DIFFERENCE: \n {yestclose_todayopen_diff}"

        api.update_status(details)

    def closing_bell():
        tickers = ["^NSEI", "^BSESN"]
        date_today = date.today()
        data = yf.download(tickers, date_today)

        today_open = data["Open"]
        today_close = data["Close"]
        print("TODAY-CLOSE")
        print(today_close)

        print("OPEN-CLOSE-DIFFERENCE")
        open_close_diff = today_close - today_open
        details = f"TODAYS CLOSE: \n {today_close} \n TODAYS OPEN CLOSE DIFFERENCE: \n {open_close_diff}"

        api.update_status(details)

        print("GRAPH DETAILS")

        def today_graph_plot():
            tickers_list = ["^NSEI", "^BSESN"]
            today_date = "2021-09-07"
            yest_date = "2021-09-06"
            data_1 = pd.DataFrame(columns=tickers_list)

            for ticker in tickers_list:
                data_1[ticker] = yf.download(ticker, yest_date, today_date)['Close']

            data_1.head()

            data.plot(figsize=(10, 7))
            plt.legend()
            plt.title("Today-Graph", fontsize=16)
            plt.ylabel('Price', fontsize=14)
            plt.xlabel('Date', fontsize=14)
            plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
            saved = plt.savefig("today_open_close.jpg")
            if saved:
                api.update_with_media("MARKETVISOR BOT/graphs/today_open_closeday")

        today_graph_plot()

    if datetime.now().hour == 9 & datetime.now().minute == (20 or 25):
        opening_bell()
    if datetime.now().hour == 15 & datetime.now().minute == (30 or 35):
        closing_bell()


def morning_greeting_with_quote():
    # Variables
    wish = "GOOD MORNING"
    quotes = ['''"An investment in knowledge pays the best interest." — Benjamin Franklin''',
              '''"Bottoms in the investment world don't end with four-year lows; they end with 10- or 15-year lows." — Jim Rogers''',
              '''"I will tell you how to become rich. Close the doors. Be fearful when others are greedy. Be greedy when others are fearful." — Warren Buffett''',
              '''"With a good perspective on history, we can have a better understanding of the past and present, and thus a clear vision of the future." — Carlos Slim Helu''',
              '''"It's not whether you're right or wrong that's important, but how much money you make when you're right and how much you lose when you're wrong." — George Soros''',
              '''"Given a 10% chance of a 100 times payoff, you should take that bet every time." — Jeff Bezos''',
              '''"Don't look for the needle in the haystack. Just buy the haystack!" — John Bogle''',
              '''"I don't look to jump over seven-foot bars; I look around for one-foot bars that I can step over." — Warren Buffett''',
              '''"The stock market is filled with individuals who know the price of everything, but the value of nothing." — Phillip Fisher''',
              '''"In investing, what is comfortable is rarely profitable." — Robert Arnott''',
              '''"How many millionaires do you know who have become wealthy by investing in savings accounts? I rest my case." — Robert G. Allen''',
              '''"If there is one common theme to the vast range of the world’s financial crises, it is that excessive debt accumulation, whether by the government, banks, corporations, or consumers, often poses greater systemic risks than it seems during a boom." — Carmen Reinhart''',
              '''"We don't prognosticate macroeconomic factors, we're looking at our companies from a bottom-up perspective on their long-run prospects of returning." — Mellody Hobson''',
              '''"Courage taught me no matter how bad a crisis gets ... any sound investment will eventually pay off." — Carlos Slim Helu''',
              '''"The individual investor should act consistently as an investor and not as a speculator." — Ben Graham''',
              '''"The biggest risk of all is not taking one." — Mellody Hobson''',
              '''"Returns matter a lot. It's our capital." — Abigail Johnson''',
              '''"It's not how much money you make, but how much money you keep, how hard it works for you, and how many generations you keep it for." — Robert Kiyosaki''',
              '''"Know what you own, and know why you own it." — Peter Lynch''',
              '''"Financial peace isn't the acquisition of stuff. It's learning to live on less than you make, so you can give money back and have money to invest. You can't win until you do this." — Dave Ramsey''',
              '''"Investing should be more like watching paint dry or watching grass grow. If you want excitement, take $800 and go to Las Vegas." — Paul Samuelson''',
              '''"The four most dangerous words in investing are, it’s different this time." — Sir John Templeton''',
              '''"Wide diversification is only required when investors do not understand what they are doing." —  Warren Buffett''',
              '''"You get recessions, you have stock market declines. If you don't understand that's going to happen, then you're not ready, you won't do well in the markets." — Peter Lynch''',
              '''"The most contrarian thing of all is not to oppose the crowd but to think for yourself." — Peter Thiel''',
              ''' “Rule #1: Don’t lose money. Rule #2: Don’t forget Rule #1.” – Warren Buffett''',
              '''“Buy not on optimism, but on arithmetic.” – Benjamin Graham''',
              ''' “Minimizing downside risk while maximizing the upside is a powerful concept.” – Mohnish Pabrai''',
              ''' “Spend each day trying to be a little wiser than you were when you woke up.” – Charlie Munger''',
              ''' “The desire to perform all the time is usually a barrier to performing over time.” – Robert Olstein''',
              '''“Risk comes from not knowing what you’re doing.”  – Warren Buffett''',
              '''“If we buy the business as a business and not as a stock speculation, then it becomes personal. I want it to be personal. – Phil Town''',
              ''' “We don’t have an analytical advantage, we just look in the right place.” – Seth Klarman''',
              ''' “No wise pilot, no matter how great his talent and experience, fails to use his checklist.” – Charlie Munger''',
              '''“I love quotes… but in the end, knowledge has to be converted to action or it’s worthless.” – Tony Robbins''',
              ''' “It is impossible to produce superior performance unless you do something different from the majority.” – John Templeton''',
              '''“The secret to investing is to figure out the value of something – and then pay a lot less.” Joel Greenblatt''',
              '''“It is remarkable how much long term advantage people like us have gotten by trying to be consistently not stupid, instead of trying to be very intelligent.” – Charlie Munger''',
              ''' “Behind every stock is a company. Find out what it’s doing.” – Peter Lynch''',
              '''“Wide diversification is only required when investors do not understand what they are doing.” – Warren Buffett''',
              ''' “Based on my own personal experience – both as an investor in recent years and an expert witness in years past – rarely do more than three or four variables really count. Everything else is noise.” – Martin Whitman''',
              ''' “Compound interest is the eighth wonder of the world. He who understands it, earns it. He who doesn’t, pays it.” – Albert Einstein''',
              ''' “I will tell you how to become rich. Close the doors, be fearful when others are greedy. Be greedy when others are fearful.” – Warren Buffett''',
              '''The individual should act consistently as an investor and not as a speculator.” Benjamin Graham''',
              '''“The entrance strategy is actually more important than the exit strategy.” – Edward Lampert''',
              '''“In many ways, the stock market is like the weather in that if you don’t like the current conditions all you have to do is wait a while.” – Low Simpson''',
              '''“The ability to focus attention on important things is a defining characteristic of intelligence.” – Robert J. Shiller''',
              ''' “Invest for the long-term.” – Lou Simpson''',
              '''“Rapidly changing industries are the enemy of the investor.” – Mohnish Pabrai''',
              '''“The easiest way to manage your money is to take it one step at a time and not worry about being perfect.” – Ramit Sethi''',
              '''“The stock market is filled with individuals who know the price of everything, but the value of nothing.” – Phillip Fisher''',
              '''“Although it’s easy to forget sometimes, a share is not a lottery ticket… it’s part ownership of a business.” – Peter Lynch''',
              ''' “All intelligent investing is value investing. Aquiring more that you are paying for. You must value the business in order to value the stock.” – Charlie Munger''',
              '''“The stock market is a device for transferring money from the impatient to the patient.” – Warren Buffett''',
              ''' “When it comes to investing, we want our money to grow with the highest rates of return, and the lowest risk possible. While there are no shortcuts to getting rich, there are smart ways to go about it.” – Phil Town''',
              ''' "In investing what is comfortable is rarely profitable." -Robert Arnott''',
              '''"Never, ever argue with your trading system." -Michael Covel''',
              '''"Amateurs think about how much money they can make. Professionals think about how much money they could lose." –Jack Schwager''',
              '''"We don't care about 'why'. Real traders only have the time and interest to care about 'what' and 'when' and 'if' and 'then'. 'Why' is for pretenders." -JC Parets''',
              '''"I'm only rich because I know when I'm wrong. I basically have survived by recognizing my mistakes." -George Soros''']

    i = list(range(60))
    random.shuffle(i)
    index_of_quotes = i.pop()
    quote = quotes[index_of_quotes]
    the_wish = f"{wish}, {quote}"

    api.update_status(the_wish)
    print("Greeted our twitter followers, BOSS.")


def book_recommendation():
    trading_books_lists = ['''The Intelligent Investor. -Benjamin Graham''',
                           '''How to make Money in Stocks. -William J. O'Neil''',
                           '''One Up on Wall Street. -Peter Lynch''',
                           '''How to avoid Loss and Earn Consistently in Stock Market. -Prasenjit Paul''',
                           '''The Truth About Day Trading Stocks. -Josh DiPetrio''',
                           '''Technical Analysis Of The Financial Markets. -John J. Murphy''',
                           '''Pit Bull: Lessons From Wall Street’s Champion Day Trader. -Martin Schwartz''',
                           '''The Big Short. -Michael Lewis''']
    i = list(range(8))
    random.shuffle(i)
    index = i.pop()
    trading_books_list = trading_books_lists[index]

    investing_books_lists = ['''A Random Walk Down Wall Street. -Burton G. Malkiel''',
                             '''The Psychology of Money. - Morgan Housel''',
                             '''The Little Book of Value Investing. -Christopher Browne''',
                             '''The WARREN BUFFET Way. -Robert G. Hangstorm''',
                             '''Rich Dad Poor Dad. -Robert Kiyosaki''',
                             '''Security Analysis. -Benjamin Graham''',
                             '''Common Stock, Uncommon Profits And Other Writings. -Philip Fisher''',
                             ''' Influence: The Psychology Of Persuasion. -Robert Cialdini''']
    j = list(range(8))
    random.shuffle(j)
    index = j.pop()
    investing_books_list = investing_books_lists[index]

    book_recommended_trading = f"Congratulations on finishing a book\n" \
                               f"I have got new recommendations\n" \
                               f"TRADING: {trading_books_list}\n" \
                               f"HAPPY READING, HAPPY LEARNING\n#Read #Learn #Invest #Trade\n"
    book_recommended_investing = f"Congratulations on finishing a book\n" \
                                 f"I have got new recommendations\n" \
                                 f"INVESTING: {investing_books_list}\n" \
                                 f"HAPPY READING, HAPPY LEARNING\n#Read #Learn #Invest #Trade\n"
    get_ebooks_free = f"Wanna get a hand on free e-books??" \
                      f"Just message me and take advantage!!\n" \
                      f"HAPPY READING, HAPPY LEARNING\n#Read #Learn #Invest #Trade #Free #Offers #Education #Help " \
                      f"#Grow #Enthusiasts #Books #selfhelp\n "
    book_recommended_trading_1 = f"TRADING: {trading_books_list}" \
                                 f"HAPPY READING, HAPPY LEARNING\n#Read #Learn #Invest #Trade\n"

    book_recommended_investing_1 = f"INVESTING: {investing_books_list}" \
                                   f"HAPPY READING, HAPPY LEARNING\n#Read #Learn #Invest #Trade\n"

    if len(book_recommended_trading) >= 230:
        api.update_status(book_recommended_trading_1)
    else:
        api.update_status(book_recommended_trading)

    if len(book_recommended_investing) >= 230:
        api.update_status(book_recommended_investing_1)
    else:
        api.update_status(book_recommended_investing)

    api.update_status(get_ebooks_free)
    print("The Book Recommendation printed, BOSS.")


def retweet_like(condition):
    while condition:
        if datetime.now().minute == (0 or 15 or 30 or 45):
            like_the_mentions()
            retweeting_market_news()
        else:
            break


while True:
    retweet_like(True)
    market_open_close_tweets()
    if datetime.now().hour == 20 & datetime.now().minute == (20 or 21):
        morning_greeting_with_quote()

    if datetime.now().weekday() == 6 & datetime.now().hour == 20 & datetime.now().minute == (20 or 21):
        book_recommendation()
        Virtual_games_recommendation()

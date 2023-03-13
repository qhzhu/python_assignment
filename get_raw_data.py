import requests
import sqlite3
import os
from sqlite3 import Error
import configparser
import os

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def symbol_request(symbol):
    """ fetch the stock price info of a specified company
        from "https://www.alphavantage.co/query"
    :param symbol: company info (IBM or APPL)
    :return: None
    """
    
    # Read API_KEY information
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(current_dir, '.env'))
        api_key = config['api']['ALPHAVANTAGE_API_KEY']
    except:
        raise Exception(
            "Unable to read ALPHAVANTAGE_API_KEY. Please check your.env file conatains ALPHAVANTAGE_API_KEY."
        )
    
    conn = None
    try:
        # api_key = os.getenv("ALPHAVANTAGE_API_KEY")

        url = "https://www.alphavantage.co/query"

        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "compact",
            "apikey": api_key
        }
        
        response = requests.get(url, params=params) 

        if response.status_code == 200:
            data = response.json()
            series = data["Time Series (Daily)"]
            db_name = os.path.join('financial', 'db.sqlite3')
            conn = create_connection(db_name)

            cursor = conn.cursor()

            for date in series.keys():
                date_data = series[date]
                open_price = date_data['1. open']
                close_price = date_data['5. adjusted close']
                volume = date_data['6. volume']
                data = (symbol, date, open_price, close_price, volume)
                cursor.execute("INSERT INTO financial_data (symbol, date, open_price, close_price, volume) VALUES (?, ?, ?, ?, ?)" , data)
                conn.commit()
            
            conn.close()
            conn = None
        else:
            print("Failed with status code:", response.status_code)

    except BaseException as ex:
        print(f'Exception was thrown: {ex}')
    finally:
        if conn is not None:
            conn.close()
            conn = None

def main():
    symbol_request("IBM")
    symbol_request("AAPL")

if __name__ == '__main__':
    main()
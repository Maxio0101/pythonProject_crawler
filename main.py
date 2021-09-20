# This is a sample Python script for stock history price.
# input: Star Date and End Date
# output: Stock history price_JsonArry
# url:https://cn.investing.com/equities/apple-computer-inc-historical-data

from __future__ import unicode_literals
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


def web_crawler(start, end):

    start_date = start
    end_date = end
    headers = {
        'Host': 'cn.investing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': "https://cn.investing.com/equities/apple-computer-inc-historical-data",
    }

    data = {
        'curr_id': '6408',
        'smlID': '1159963',
        'header': 'AAPL历史数据',
        'st_date': start_date,
        'end_date': end_date,
        'interval_sec': 'Daily',
        'sort_col': 'date',
        'sort_ord': 'ASC',
        'action': 'historical_data',
    }
    url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
    resp = requests.post(url, data=data, headers=headers)
    htm = resp.text.encode("utf-8")
    #print(resp.text)
    page = BeautifulSoup(htm, 'lxml')
    #stocks_result_table = page.find('table', 'genTbl closedTbl historicalTbl').tbody.find_all('tr')
    stocks_result = page.find('table', 'genTbl closedTbl historicalTbl')
    #found_data = stocks_result_table.tbody.find('td', attrs={'class':'first left bold noWrap'})
    #if found_data: #stocks_list = page.find('table', 'genTbl closedTbl historicalTbl')
        #Result_formation(stocks_list)
    #else:
        #print('No results found...')

    #print(stocks_result)


    return stocks_result

def Result_formation(stocks_result):
    result_list = []
    found_data = stocks_result.tbody.find('td', attrs={'class': 'first left bold noWrap'})
    if not found_data:
        result_list =['No results found...']
    else:
    # result_dic = {}
        stocks_result_table = stocks_result.tbody.find_all('tr')
        for row in stocks_result_table:
            result_dic = {}
            result_dic['Date'] = row.find_all('td')[0].text
            result_dic['Price'] = row.find_all('td')[1].text
            result_dic['Open'] = row.find_all('td')[2].text
            result_dic['High'] = row.find_all('td')[3].text
            result_dic['Low'] = row.find_all('td')[4].text
            result_dic['Vol'] = row.find_all('td')[5].text
            result_list.append(result_dic)

    #print("result_list:", type(result_list))
    result_json = json.dumps(result_list, ensure_ascii=False)
    #print('result_list:', result_json)
    #print(type(result_json))
    return result_json

# Press the green button in the gutter to run the script.

def validate_date(d):
    try:
        datetime.strptime(d, '%Y/%m/%d')
        return True
    except ValueError:
        return False



if __name__ == '__main__':
    start = input("Start Date input:(yyyy/mm/dd)")
    start_date_check_ok = validate_date(start)
    end = input("End Date input:(yyyy/mm/dd)")
    end_date_check_ok = validate_date(end)

    if start_date_check_ok and end_date_check_ok:
        result_json = web_crawler(start, end)
        Result_formation(result_json)
        print(Result_formation(result_json))
    else:
        print('Date formation error!!')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

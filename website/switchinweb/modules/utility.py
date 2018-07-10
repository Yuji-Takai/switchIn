from datetime import datetime

""" converts the string extracted from text to date
:param date:    string representing the date
:returns:       datetime for the string
"""
def convertDateFormat(date):
    if (len(date) == 8):
        month = date[0:2]
        day = date[3:5]
        year = date[6:len(date)]
        year = "19" + year if int(year) > 50 else "20" + year
        date = year + "-" + month + "-" + day
        return datetime.strptime(date, '%Y-%m-%d')
    return ""

def str_to_num(money):
    if (money):
        money = money.split(",")
        new_money = ""
        for num in money:
            new_money = new_money + num
        return int(new_money[1:len(new_money)])
    return 0




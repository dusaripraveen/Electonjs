from datetime import datetime, timedelta


def format_date(input_date):
    new_dates = []
    for date in input_date:
        input_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M") - timedelta(days=1)
        start_date = check_date_format(input_datetime.strftime("%b%d"))
        end_date_formatted = input_datetime - timedelta(days=6)
        end_date = check_date_format(end_date_formatted.strftime("%b%d"))
        new_dates.append(f"{end_date}-{start_date}")
    return new_dates


def format_month(input_month):
    new_mon = []
    for month in input_month:
        input_mon = datetime.strptime(month, "%Y-%m-%d %H:%M")
        month = input_mon.strftime("%b")
        new_mon.append(month)
    return new_mon


def check_date_format(date):
    if date[3] == '0':
        return date[:3] + date[4:]
    else:
        return date


def acom_store(data):
    if 'PROD' in data:
        return 'Store Actual'
    elif 'ACOM' in data:
        return 'ACOM Home Actual'
    else:
        return data


def online_monthly(data):
    if 'SanJose' in data:
        return 'US-San Jose (SLA - 21 s)'
    elif 'Frankurt' in data:
        return 'Germany- Frankurt (SLA - 23 s)'
    elif 'Beijing' in data:
        return 'China - Beijing (SLA - 3s)'
    else:
        return data


def acom_monthly(data):
    if 'SanJose' in data:
        return 'US-San Jose (SLA - 3 s)'
    elif 'Page_Frankfurt' in data:
        return 'Germany- Frankfurt (SLA - 3.5 s)'
    elif 'Beijing' in data:
        return 'China - Beijing (SLA - 3 s)'
    else:
        return data


def aem_label_format(data):
    if 'Home Page' in data:
        return 'Landing Page'
    elif 'Sign In' in data:
        return 'Login Page'
    elif 'Search' in data:
        return 'Search'
    elif 'Logout' in data:
        return 'Logout'
    else:
        return data


def acom_store_sla(sla, data, value, length):
    data[sla] = [value] * length

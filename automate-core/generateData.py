import os
import constants
import pandas as pd
import json
from formatcsv import acom_store, acom_store_sla, format_date, online_monthly, acom_monthly, format_month, \
    aem_label_format


def generate_data(file_path, report_type):
    data = {}
    df = pd.read_csv(file_path)
    json_data = json.loads(df.to_json())
    if report_type == 'acom_online':
        acom_online_generate(data, json_data, report_type)
    elif report_type == 'acom_monthly' or report_type == 'online_monthly':
        acom_online_monthly_generate(data, json_data, report_type)
    elif report_type == 'aem_us' or report_type == 'aem_germany' or report_type == 'aem_china':
        aem_monthly_generate(data, json_data, report_type)
    print(f"final output --> {data}")
    return data


def acom_online_generate(data, json_data, report_type):
    acom_store_sla('ACOM Home SLA', data, 1.43, 4)
    acom_store_sla('Store SLA', data, 21, 4)
    for key in list(json_data.keys()):
        data[acom_store(key)] = list(json_data[key].values())
    data['name'] = constants.data_obj[report_type]['name']
    data['Date'] = format_date(data['Date'])
    return data


def online_monthly_generate(data, json_data, report_type):
    for key in list(json_data.keys()):
        data[online_monthly(key)] = list(json_data[key].values())
    data['name'] = constants.data_obj[report_type]['name']
    data['Date'] = format_month(data['Date'])
    return data


def acom_online_monthly_generate(data, json_data, report_type):
    for key in list(json_data.keys()):
        if report_type == 'acom_monthly':
            data[acom_monthly(key)] = list(json_data[key].values())
        elif report_type == 'online_monthly':
            data[online_monthly(key)] = list(json_data[key].values())
    data['name'] = constants.data_obj[report_type]['name']
    data['Date'] = format_month(data['Date'])
    return data


def aem_monthly_generate(data, json_data, report_type):
    for key in list(json_data.keys()):
        data[aem_label_format(key)] = list(json_data[key].values())
    data['name'] = constants.data_obj[report_type]['name']
    data['Date'] = format_date(data['Date'])
    return data


path = "./input/aem.csv"
generate_data(path, 'aem_us')

# path = "./input/visually-monthly-acom.csv"
# generate_data(path, 'acom_monthly')
#
# path = "./input/Graph.csv"
# generate_data(path, 'acom_online')

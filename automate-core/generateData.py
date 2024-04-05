import os
import constants
import pandas as pd
import json
from formatcsv import acom_store, acom_store_sla, format_date, online_monthly, acom_monthly, format_month, \
    aem_label_format, ms_conversion

from generateExcel import generate_excel_and_chart


def generate_data(file_path, report_type):
    data = {}
    df = pd.read_csv(file_path)
    json_data = json.loads(df.to_json())
    if report_type == 'acom_online':
        acom_online_generate(data, json_data, report_type)
    elif report_type == 'acom_monthly':
        acom_online_monthly_generate(data, json_data, report_type)
    elif report_type == 'online_store_monthly':
        online_monthly_generate(data, json_data, report_type)
    elif report_type == 'aem_us' or report_type == 'aem_germany' or report_type == 'aem_china':
        aem_monthly_generate(data, json_data, report_type)
    print(f"final output --> {data}")
    return data


def acom_online_generate(data, json_data, report_type):
    acom_store_sla('ACOM Home SLA', data, 1.43, 4)
    acom_store_sla('Store SLA', data, 21, 4)
    core_data = {}
    for key in list(json_data.keys()):
        core_data[acom_store(key)] = list(json_data[key].values())
    core_data['Date'] = format_date(core_data['Date'])
    data['name'] = constants.data_obj[report_type]['name']
    data['data'] = core_data
    return data


def online_monthly_generate(data, json_data, report_type):
    core_data = {}
    for key in list(json_data.keys()):
        if 'Frankfurt' in key:
            core_data['Germany- Frankurt (SLA - 23 s)'] = ms_conversion(list(json_data[key].values()))
        else:
            core_data[online_monthly(key)] = list(json_data[key].values())
    core_data['Date'] = format_month(core_data['Date'])
    data['name'] = constants.data_obj[report_type]['name']
    data['data'] = core_data
    return data


def acom_online_monthly_generate(data, json_data, report_type):
    core_data = {}
    for key in list(json_data.keys()):
        if report_type == 'acom_monthly':
            core_data[acom_monthly(key)] = list(json_data[key].values())
        elif report_type == 'online_store_monthly':
            core_data[online_monthly(key)] = list(json_data[key].values())
    core_data['Date'] = format_month(core_data['Date'])
    data['name'] = constants.data_obj[report_type]['name']
    data['data'] = core_data
    return data


def aem_monthly_generate(data, json_data, report_type):
    core_data = {}
    for key in list(json_data.keys()):
        core_data[aem_label_format(key)] = list(json_data[key].values())
    core_data['Date'] = format_date(core_data['Date'])
    data['name'] = constants.data_obj[report_type]['name']
    data['data'] = core_data
    return data


def get_excel():
    dir_path = "./input/csv_inputs/"
    excel_name = './output/sample1.xlsx'
    dir_list = os.listdir(dir_path)
    print(f'list of files -->  {dir_list}')
    reports_arr = []
    for dir_name in dir_list:
        file_name, file_extension = os.path.splitext(dir_name)
        print(f'file path --> {file_extension}')
        print(f'file name --> {file_name}')
        if file_extension == '.csv':
            file_path = dir_path + dir_name
            data = generate_data(file_path, file_name)
            reports_arr.append(data)
    print(f"final reports ---> {reports_arr}")
    result = generate_excel_and_chart(reports_arr, excel_name)
    if result['status']:
        return result
    return {
        'status': False,
        'message' : 'error'
    }


# path = "./input/aem.csv"
# generate_data(path, 'aem_us')

# path = "./input/visually-monthly-acom.csv"
# generate_data(path, 'acom_monthly')
#
# path = "./input/Graph.csv"
# generate_data(path, 'acom_online')

# path = "./input/neew_inputs/online_store_monthly.csv"
# generate_data(path, 'online_store_monthly')

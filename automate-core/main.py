import argparse

from automation import automate_chrome
import os
import shutil
from constants import acom_online, aem_monthly, user_details
from generateData import get_excel
from pathlib import Path


def get_urls_acom_online():
    arr = []
    for key, value in acom_online.items():
        arr.append({
            'report_name': key,
            'data': value
        })
    return arr


def get_urls_aem():
    arr = []
    for key, value in aem_monthly.items():
        arr.append({
            'report_name': key,
            'data': value
        })
    return arr


def start(email, password, dyntrc_data, report):
    for dy_data in dyntrc_data:
        print(dy_data)
        automate_chrome(dy_data, email, password)
        get_csv(dy_data['report_name'], report)
    print('initiating excel generation')
    result = get_excel(report)
    if result['status']:
        print('success')
        clear_data()
    else:
        print("Process failed")


def start_process(email, password, report):
    if report == 'weekly':
        # weekly data
        dyntrc_data_acom = get_urls_acom_online()
        start(email, password, dyntrc_data_acom, 'weekly')
    elif report == 'monthly':
        # weekly data
        dyntrc_data_acom = get_urls_acom_online()
        start(email, password, dyntrc_data_acom, 'weekly')

        # monthly data
        dyntrc_data_aem = get_urls_aem()
        start(email, password, dyntrc_data_aem, 'monthly')


def get_csv(new_name, report):
    downloads_folder = os.path.expanduser("~/Downloads")
    custom_folder = './input/csv_inputs/' + report + '/'

    Path(custom_folder).mkdir(parents=True, exist_ok=True)

    files = [f for f in os.listdir(downloads_folder) if os.path.isfile(os.path.join(downloads_folder, f))]
    most_recent_file = max(files, key=lambda f: os.path.getctime(os.path.join(downloads_folder, f)))

    if not files:
        print("No files found in Downloads folder")
    else:

        # split file name and extension
        file_name, file_extension = os.path.splitext(most_recent_file)

        # change file name
        source_path = os.path.join(downloads_folder, most_recent_file)
        destination_path = os.path.join(custom_folder, new_name + file_extension)

        try:
            shutil.move(source_path, destination_path)
            print(f"file moved to {custom_folder} from {downloads_folder} as {new_name}")
        except Exception as e:
            print(f"Error moving file {e}")


def clear_data():
    dir_path = "./input/csv_inputs/"

    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting filepath {file_name}: {e}")


def main():
    parser = argparse.ArgumentParser(description='process some user inputs')
    parser.add_argument('--email', type=str, help='User name')
    parser.add_argument('--password', type=str, help='User Password')
    parser.add_argument('--report', type=str, choices=['weekly', 'monthly'])

    args = parser.parse_args()

    if args.email is None or args.password is None or args.report is None:
        print("please provide valid details")
        return
    print('User name - ', args.email)
    print('Password - ', args.name)
    print('report - ', args.report)
    start_process(args.email, args.password, args.report)


# if __name__ == "__main__":
#     main()

start_process(user_details['email'], user_details['password'], 'monthly')
# start()

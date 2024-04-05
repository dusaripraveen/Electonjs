from automation import automate_chrome
import os
import shutil
import constants
from generateData import get_excel


def get_urls():
    arr = []
    for key, value in constants.data_obj.items():
        arr.append({
            'report_name': key,
            'data': value
        })
    return arr


def start():
    dynatrace_data = get_urls()
    for dy_data in dynatrace_data:
        print(dy_data)
        automate_chrome(dy_data, constants.user_details['email'], constants.user_details['password'])
        get_csv(dy_data['report_name'])
    print('initiating excel generation')
    result = get_excel()
    if result['status']:
        clear_data()
    else:
        print("Process failed")


def get_csv(new_name):
    downloads_folder = os.path.expanduser("~/Downloads")
    custom_folder = './input/csv_inputs/'

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
        except Exception as e:
            print(f"Error deleting filepath {file_name}: {e}")


start()

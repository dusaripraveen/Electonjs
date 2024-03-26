import pandas as pd
import sys 
def generate_excel_and_chart(json_data, excel_filename):
    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter') # Create excel writer

    for data in json_data:
        df = pd.DataFrame(data) # Create DataFrame
        col = len(data["data"])+10
        # Writer DataFrame to Excel
        df.to_excel(writer, sheet_name='Data', index=False, startrow=0, startcol=0)

    #Add a chart to the existing sheet
    workbook = writer.book
    worksheet = writer.sheets['Data'] #sheet name

    #create a line chart
    chart = workbook.add_chart({'type': 'line'})

    # configure the series for Hotel A
    chart.add_series({
        'name': '=Data!$B$1', # Hotel A
        'categories': ['Data', 1, 0, len(df), 0], # data column as x-axis
        'values': ['Data', 1, 1, len(df), 1], # visitors columns as y-axis
        'markers': { # custom marker style
            'type': 'circle',
            'size': 7,
            'border': {
                'color': 'black'
            },
            'fill': {
                'color': 'red'
            }
        },
        'data_labels': { # show data labels
            'value': True,
            'font': {
                'bold': True,
                'color': 'black'
            }
        }
    })

    # configure the series for Hotel B
    chart.add_series({
        'name': '=Data!$C$1', # Hotel B
        'categories': ['Data', 1, 0, len(df), 0], # data column as x-axis
        'values': ['Data', 1, 2, len(df), 2], # visitors columns as y-axis
        'markers': { # custom marker style
            'type': 'circle',
            'size': 7,
            'border': {
                'color': 'black'
            },
            'fill': {
                'color': 'blue'
            }
        },
        'data_labels': { # show data labels
            'value': True,
            'font': {
                'bold': True,
                'color': 'black'
            }
        }
    })

    # Remove grid lines
    chart.set_x_axis({'major_gridlines': {'visible': False}})
    chart.set_y_axis({'major_gridlines': {'visible': True}})

    chart.set_legend({'position': 'bottom'})
    chart.set_title({'name': 'Hotel Comparison'})
    # Insert the chart into the existing worksheet
    worksheet.insert_chart('A10', chart)

    # Close the Pandas Excel writter and save the Excel file
    writer._save()


def main():
    # Sample JSON data for two hotels
    print("main function")
    json_data = [{
        "name": "Hotel Comparison",
        "data": ["Week1","Week2","Week3","Week4","Week5"],
        "Hotel A": [100, 120, 90, 110, 130],
        "Hotel B": [90, 110, 100, 120, 110],
        "Hotel C": [21, 21, 21, 21, 21],
        "Hotel D": [3, 3, 3, 3, 3],
    },
        {
            "name": "Bank comparison",
            "data": ["Week1", "Week2", "Week3", "Week4", "Week5"],
            "Hotel A": [10, 12, 9, 11, 13],
            "Hotel B": [9, 11, 10, 12, 10],
            "Hotel C": [21, 21, 21, 21, 21],
            "Hotel D": [3, 3, 3, 3, 3],
        }]

    # specify the filename for the excel file
    excel_filname = './hotel_data.xlsx'

    # Generate Excel and chart
    generate_excel_and_chart(json_data, excel_filname)
    print(f'Excel file with data and chart saved as {excel_filname}')

if __name__ == "__main__":
    main()
    sys.stdout.flush()


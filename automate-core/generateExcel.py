import pandas as pd


def generate_excel_and_chart(data_list, excel_filename):
    # create excel writer
    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')

    # create a workbook
    workbook = writer.book

    # Add a worksheet
    worksheet = workbook.add_worksheet('Data')

    # Track row number and starting column for inserting tables and charts
    row_num = 0
    start_col = 0

    # Format for the table border
    border_format = workbook.add_format({'border': 1})

    # Loop through each dataset
    for idx, data in enumerate(data_list):
        print(f"data --> {data}")
        # covert json into dataframe
        df = pd.DataFrame(data['data'])

        # write dataframe into excel
        df.to_excel(writer, sheet_name='Data', startrow=row_num, startcol=start_col, index=False)

        # table styling
        end_row = row_num + len(df)
        end_col = start_col + df.shape[1] - 1
        worksheet.conditional_format(row_num, start_col, end_row, end_col,
                                     {'type': 'no_blanks', 'format': border_format})

        # create line chart
        chart = workbook.add_chart({'type': 'line'})
        # colors = ['#FFA500', '#ADD8E6', '#008000', '#000080']
        # configure the series
        for col in range(1, len(df.columns)):
            chart.add_series({
                'name': f'=Data!${chr(ord("A") + start_col + col)}$1',
                'categories': ['Data', row_num + 1, start_col, row_num + len(df), start_col],
                'values': ['Data', row_num + 1, start_col + col, row_num + len(df), start_col + col],
                'marker': {'type': 'circle', 'size': 5},
                'data_labels': {'value': True},
                # 'line': {'color': colors[col-1]}
            })
        # y-axis properties
        chart.set_y_axis({'visible': True,
                          'line': {'none': True},
                          'label_position': 'center'
                          })

        # x-axis properties
        chart.set_x_axis({
            'label_position': 'center'
        })

        # legend properties
        chart.set_legend({'position': 'bottom'})
        chart.set_title({'name': data['name']})

        # insert chart into Excel
        worksheet.insert_chart(row_num + df.shape[0] + 5, start_col, chart)

        start_col += df.shape[1] + 7

    writer._save()
    return {
        'status': True,
        'message': "File downloaded"
    }

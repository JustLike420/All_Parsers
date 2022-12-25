def convert_workbook(filename: str):
    from openpyxl import Workbook
    import csv
    wb = Workbook()
    ws = wb.active
    with open(f'{filename}.csv', 'r') as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save(f'{filename}.xlsx')
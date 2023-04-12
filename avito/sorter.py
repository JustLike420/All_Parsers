import openpyxl

wb = openpyxl.load_workbook('result1.xlsx')

sheet = wb.active
data = {
    'Количество гостей:': None,
    'Можно с детьми:': None,
    'Можно с животными:': None,
    'Можно курить:': None,
    'Разрешены вечеринки:': None,
    'Есть отчётные документы:': None,
    'Количество комнат:': None,
    'Общая площадь:': None,
    'Этаж:': None,
    'Техника:': None,
    'Интернет и ТВ:': None,
    'Комфорт:': None,
    'Залог:': None,
}
for row in sheet.iter_rows():
    for col in row:
        print(col.value)
    break

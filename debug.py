import pandas as pd

# 讀取 Excel 檔案
xlsx_path = r"C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\02_Document\ADI\WeeklyReport\WeeklyReport_Bruce.xlsx"
xls = pd.ExcelFile(xlsx_path)

# 列出所有 Sheet 名稱
# print(xls.sheet_names)
[print(i) for i in xls.sheet_names]

# import openpyxl

# # 開啟 Excel 檔案
# xlsx_path = "your_file.xlsx"
# wb = openpyxl.load_workbook(xlsx_path)

# # 列出所有 Sheet 名稱
# sheet_names = wb.sheetnames
# print(sheet_names)
# [print(i) for i in sheet_names]

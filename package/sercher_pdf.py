import os
import time
from PyPDF2 import PdfReader

def search_pdf_keyword(directory, keyword, filename_filter):
    results = {}
    # 遍歷所有子目錄
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 檢查副檔名是否為 PDF
            if file.lower().endswith('.pdf'):
                # 若有設定檔名 filter，且檔名中不包含 filter 關鍵字，則跳過
                if filename_filter and filename_filter.lower() not in file.lower():
                    continue
                pdf_path = os.path.join(root, file)
                try:
                    reader = PdfReader(pdf_path)
                    pages_with_keyword = []
                    # 逐頁讀取並檢查是否包含關鍵字
                    for page_num, page in enumerate(reader.pages, start=1):
                        text = page.extract_text()
                        if text and keyword.lower() in text.lower():
                            pages_with_keyword.append(page_num)
                    if pages_with_keyword:
                        results[pdf_path] = pages_with_keyword
                except Exception as e:
                    print(f"處理 {pdf_path} 時發生錯誤：{e}")
    return results

if __name__ == "__main__":
    directory = input("請輸入目錄路徑：")
    keyword = input("請輸入要搜尋的關鍵字：")
    filename_filter = input("請輸入檔名篩選關鍵字（留空表示不篩選）：")
    
    # 記錄開始時間
    start_time = time.time()
    
    found = search_pdf_keyword(directory, keyword, filename_filter)
    
    # 記錄結束時間
    end_time = time.time()
    total_time = end_time - start_time
    
    if found:
        for pdf, pages in found.items():
            print(f"在文件：{pdf} 中，關鍵字「{keyword}」出現在第 {pages} 頁")
    else:
        print("未找到符合的關鍵字。")
    
    # 輸出總花費時間
    print(f"總花費時間：{total_time:.2f} 秒")

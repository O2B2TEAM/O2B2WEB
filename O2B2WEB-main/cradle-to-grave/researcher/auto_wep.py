import os
import time

from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def create_datadigester_folder():
    """다운로드 받을 폴더 생성"""
    c_drive = "C:\\"
    folder_name = "노세"
    count = 1
    while True:
        new_folder_name = folder_name if count == 1 else f"{folder_name}_{count}"
        new_folder_path = os.path.join(c_drive, new_folder_name)
        if not os.path.exists(new_folder_path):
            break
        count += 1
    
    try:
        os.mkdir(new_folder_path)
        print(f"'{new_folder_name}' 폴더가 성공적으로 생성되었습니다.")
    except PermissionError:
        print("권한이 없어 폴더를 생성할 수 없습니다.")
    
    return new_folder_path

def set_download_path(download_dir):
    """PDF 다운로드 경로 설정"""
    download_path = os.path.join(download_dir, "downloads")
    if not os.path.exists(download_path):
        os.mkdir(download_path)
        print(f"다운로드 경로 '{download_path}'가 설정되었습니다.")
    else:
        print(f"다운로드 경로 '{download_path}'가 이미 존재합니다.")

def download_pdf_and_extract_text(query):
    """PDF 다운로드 및 텍스트 추출"""
    download_dir = create_datadigester_folder()
    set_download_path(download_dir)
    
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.path.join(download_dir, "downloads"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://scholar.google.co.kr/schhp?hl=ko')

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)  # 입력된 쿼리로 검색
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)

    pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'pdf')]")
    
    for link in pdf_links:
        link.click()
        time.sleep(5)

    driver.quit()

    downloaded_files = [get_latest_downloaded_file(download_dir) for _ in pdf_links]
    pdf_texts = [extract_text_from_pdf(file_path) for file_path in downloaded_files]    
    # 여러 PDF 파일의 텍스트를 하나의 문자열로 합침
    combined_text = "\n".join(pdf_texts)
    
    return combined_text

def extract_text_from_pdf(pdf_path):
    """PDF에서 텍스트 추출"""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def get_latest_downloaded_file(download_dir):
    """가장 최근에 다운로드된 파일 경로 반환"""
    list_of_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

if __name__ == "__main__":
    # 검색어를 받아 PDF를 다운로드하고 텍스트를 추출하여 출력
    query = input("검색어를 입력하세요: ")
    pdf_text = download_pdf_and_extract_text(query)
    print(pdf_text)

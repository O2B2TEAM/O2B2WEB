### 20240616 cradle-to-grave 폴더 업데이트

1) job 폴더와 home 폴더 우선으로 변경 해 주세요. 다른 폴더는 아직 업데이트 되지 않았습니다.

2) requirements.txt 파일 설치 시 기존 라이브러리들 uninstall 하고 설치 해 주세요.
    ai_interview.py 의 chromaDB 라이브러리와 충돌 발생합니다.

3) image 폴더,fonts 폴더, .streamlit 폴더의 toml 파일 추가되었습니다.

4) pdf_download.py 등 pdf 파일 다운로더 기능은 어느 서버에서나 실행 가능하도록 변경 중이에요. 오류가 뜨더라도 정상입니다.

### 디렉토리 폴더 구조
#### home
![image](https://github.com/O2B2TEAM/O2B2WEB/assets/112530099/d6c3b0e4-69f7-4201-af55-eaa58cda64ec)

#### job
![image](https://github.com/O2B2TEAM/O2B2WEB/assets/112530099/4233ef76-5797-4c90-b973-075234873d07)

#### .gitignore
#### .env
![image](https://github.com/O2B2TEAM/O2B2WEB/assets/112530099/3bcb09f5-80ab-4b6b-837e-29ee76f926a4)

#### .env 내용
[theme]
primaryColor="#ff9000"
backgroundColor="#ffffff"
secondaryBackgroundColor="#fffcee"
textColor="#523500"
font = "sans serif"

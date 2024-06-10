import numpy as np
import pandas as pd
import streamlit as st

st.title("노인복지 사이트 모아보기")
st.text("description :공기관에서 추천해주는 페이지들과 연계 (모아보기 기능)")
st.text("search bar")
st.text("조건 선택")
st.text("사이트 뷰 박스 (박스 안에는 사이트 이미지와 정보)")

st.text("노인 일자리 전국 수행 기관")
st.text("검색하기")


name=['구분','양로시설 시설수','양로시설 정원','양로시설 현원','노인공동생활가정 시설수','노인공동생활가정 정원',	'노인공동생활가정 현원',	'노인요양시설 시설수',	'노인장기요양법에 의한 미지정 노인요양시설수',	'노인요양시설 정원',	'노인장기요양법에 의한 미지정 노인요양시설정원',	'노인요양시설 현원',	'노인장기요양법에 의한 미지정 노인요양시설현원',	'노인요양공동생활가정 시설수',	'노인장기요양법에 의한 미지정 노인요양공동생활가정시설수',	'노인요양공동생활가정 정원',	'노인장기요양법에 의한 미지정 노인요양공동생활가정시설정원',	'노인요양공동생활가정 현원',	'노인장기요양법에 의한 미지정 노인요양공동생활가정시설현원'
]
#데이터프레임 형식으로 저장
csv = pd.read_csv("dir/file1.csv", sep=",", encoding='utf-8')

df1=pd.append([name,csv])
st.dataframe(df1)
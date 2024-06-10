#!/bin/sh

# 각 애플리케이션을 백그라운드에서 실행
streamlit run /cradle-to-grave/home_before_login.py --server.port=8501 --server.address=0.0.0.0 &
streamlit run /cradle-to-grave/kid_gamification.py --server.port=8502 --server.address=0.0.0.0 &
streamlit run /cradle-to-grave/public_organization.py --server.port=8503 --server.address=0.0.0.0 &
streamlit run /cradle-to-grave/main.py --server.port=8504 --server.address=0.0.0.0 &
streamlit run /cradle-to-grave/digester_intern.py --server.port=8505 --server.address=0.0.0.0 &
streamlit run /cradle-to-grave/welfare.py --server.port=8506 --server.address=0.0.0.0 &
streamlit run /cradle-to-grave/job_selector.py --server.port=8507 --server.address=0.0.0.0 &

# 컨테이너를 계속 실행 상태로 유지
wait

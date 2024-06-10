# Use an appropriate base image
# 적절한 베이스 이미지 사용
FROM python:3.9-slim

# Set the working directory 
# 작업 디렉토리 설정
WORKDIR /job

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the content of the home directory into the container. 
# home 디렉토리 내용을 컨테이너로 복사
COPY . /job

RUN pip3 install -r requirements.txt

# # 필요한 의존성 설치
RUN pip install streamlit

EXPOSE 8507

HEALTHCHECK CMD curl --fail http://localhost:8507/_stcore/health

ENTRYPOINT ["streamlit", "run", "job_selector.py", "--server.port=8507"]

FROM python:3.8

WORKDIR /seabot_wx

COPY ./requirements.txt .

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "./Main.py"]
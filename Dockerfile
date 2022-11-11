FROM harbor.rongzer.net/common/py39-allure:1.0.0

WORKDIR .

ADD . .

CMD ["python", "main.py"]
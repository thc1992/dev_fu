本框架采用  python3+pytest_allure_yaml+钉钉通知


下载allure配置allure环境，不然无法生成allure报告

验证allure安装和配置成功使用

allure --version


配置为文件缺什么自己手动安装
通过 pip3 install *


通过命令生成可视化报告

allure generate ./allure-results   -o    ./report/html     --clean

直接运行生成报告资源

python  main.py


钉钉通知：是读取自动化跑测的结果，推送到钉钉消息

allure报告显示：
![image](https://user-images.githubusercontent.com/19609770/188765071-c984b5f2-16bb-41b1-96c0-9c8b43f6a2df.png)










# 电视/游戏使用时长定时提醒（小米生态）

监测智能插座实时功率，如果 `实时功率>50w` 则认为电视开启。在 `15分钟` 时利用 `小爱音箱` 进行第一次提醒，此后每5分钟提醒一次观看时间。

## 环境依赖

- Python >= 3.8

## 设置说明

1. 安装依赖
    ```shell
    # 安装 poetry
    pip install poetry
    # 安装依赖库
    poetry install --only=main
    ```
2. 查询设备 `did`
    ```shell
    export MI_USER=小米账号
    export MI_PASS=小米账号密码
    # 显示该账号下的设备列表，找到音箱和插座的did
    micli.py list
    ```
3. 创建配置文件 `.env`
    ```shell
    cp sample.env .env
    ```
4. 编辑配置文件
    ```shell
    MI_USER=小米账号
    MI_PASS=小米账号密码
    SPEAKER_DID=音箱did
    PLUG_DID=插座did
    ```
5. 运行程序
    ```shell
    poetry run python cheep_app.py
    ```

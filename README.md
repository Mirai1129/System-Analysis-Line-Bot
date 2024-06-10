# 長照系統 Line Bot

## 專案背景

本專案旨在建立一個長照系統，為需要長期照護服務的人群提供便捷的資訊查詢和預約服務。該系統結合了 Web 應用和 Line Bot
兩種形式，用戶可以通過網站登錄查詢相關資訊，也可以通過 Line Bot 進行快捷的資訊查詢和預約操作。

## 功能特點

1. **資訊查詢**:
    - 用戶可以通過 Web 應用或 Line Bot 查詢照護人員訊息、營業時間、地址等相關資訊。

2. **預約服務**:
    - 用戶可以通過 Line Bot 進行預約服務，系統將根據用戶提供的資訊安排相應的服務，用戶也可以通過預約表單進行服務預約。

3. **照護人員資訊**:
    - 系統提供照護人員的詳細資訊，用戶可以查看其個人資料和社交媒體鏈接，以便更好地了解服務人員。

## 技術實現

1. **Flask Web 應用**:
    - 使用 Flask 框架構建 Web 應用，提供用戶登錄、資訊查詢、預約服務等功能。

2. **Line Bot 交互**:
    - 通過 Line Bot 與用戶進行交互，提供資訊查詢、預約服務等功能，使用戶可以通過 Line 平臺方便地獲取所需服務。

3. **MongoDB 數據庫**:
    - 使用 MongoDB 存儲用戶資訊、照護人員數據以及預約記錄等資訊，保證數據的持久性和可擴展性。

## 快速開始

1. **安裝套件**:
    - 使用 `requirements.txt` 安裝專案所需的 Python 套件：
      ```
      pip install -r requirements.txt
      ```

2. **設置環境變量**:
    - 將 `.exampleenv` 文件重命名為 `.env`，並填寫相應的配置資訊，包括 Line Bot 的 Channel Secret 和 Access Token，以及
      MongoDB 的連接資訊。

3. **運行 MongoDB 服務**:
    - 使用 Docker 啟動 MongoDB 服務：
      ```
      docker-compose up -d
      ```

4. **啟動應用**:
    - 運行 Flask 應用：
      ```
      python app.py
      ```

## 專案結構

```
├── app.py
├── database/
│   ├── Members/
│   │   ├── __init__.py
│   │   ├── adapter/
│   │   │   ├── MongoAdapter.py
│   │   │   ├── MongoBuilder.py
│   │   │   └── MongoChecker.py
├── Members/
│   ├── __init__.py
│   ├── members.py
│   ├── static/
│   └── templates/
├── modules/
│   ├── __init__.py
│   ├── caregivers.py
│   ├── commands.py
│   └── sampledataset.py
├── static/
├── templates/
├── .gitignore
├── .exampleenv
├── README.md
├── requirements.txt
├── docker-compose.yml
└── Dockerfile

```

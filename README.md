# Wahoo - 智慧型 NLP 聊天機器人引擎

Wahoo 是一個功能強大的自然語言處理 (NLP) 聊天機器人引擎，旨在理解並回應中文使用者的各種查詢。它整合了意圖分類、實體抽取、上下文管理和答案生成等多個模組，為開發者提供了一個完整、可擴展的對話式 AI 解決方案。

## 系統架構

本引擎採用模組化架構，將複雜的 NLP 任務拆解為清晰定義的元件，使其易於維護和擴展。

![NLP Platform Architecture](Architectures/NLP_Platform_Architecture.pdf)

其核心處理流程如下：

1.  **接收請求 (Tornado Server)**：使用 Tornado 建立非同步 Web 服務器，接收來自客戶端的 HTTP 請求。
2.  **意圖分類 (Intent Classifier)**：利用基於羅吉斯迴歸的模型，分析使用者輸入的文本，判斷其主要意圖 (例如：查詢天氣、播放音樂、導航等)。
3.  **實體抽取 (Dissection Engine)**：根據判斷出的意圖，從文本中精確提取關鍵資訊 (實體)，例如地點、時間、歌曲名稱等。
4.  **上下文管理 (Context Manager)**：在多輪對話中追蹤和管理使用者的狀態和先前對話的資訊，以實現更流暢、更自然的互動。
5.  **答案生成 (Answer Formatter)**：根據意圖和抽取的實體，從後端服務或資料庫查詢相關資訊，並將其格式化為人類可讀的自然語言回答。
6.  **回傳響應**：將生成的答案透過 API 回傳給使用者。

## 核心功能

- **多領域支援**：內建多種常見的生活化領域，包括：
    - **天氣查詢** (`Weather`)
    - **音樂播放** (`Music`)
    - **新聞瀏覽** (`News`)
    - **股票查詢** (`Stock`)
    - **火車時刻** (`Train`)
    - **導航** (`Navigation`)
    - **叫計程車** (`Taxi`)
    - **附近景點** (`Tour`)
    - **醫院資訊** (`Hospital`)
    - **百科查詢** (`Wiki`)
    - **一般聊天** (`Chat`)
- **意圖辨識**：高準確度的意圖分類模型，能理解使用者的指令。
- **實體抽取**：基於規則和字典的實體提取方法，能精準抓取關鍵字。
- **上下文管理**：支援多輪對話，能夠理解關聯性查詢。
- **可擴展性**：模組化的設計讓新增意圖、實體和答案格式變得非常容易。

## 快速入門

請依照以下步驟在您的本機環境中設定和執行 Wahoo 引擎。

### 1. 環境要求

- Python 3.x
- pip

### 2. 安裝相依套件

複製本專案後，進入專案根目錄，並執行以下指令以安裝所有必要的函式庫：

```bash
pip install -r requirements.txt
```

3. 執行服務
安裝完成後，執行 TornadoServer.py 來啟動後端 API 服務。

```bash
python TornadoServer.py
```

預設情況下，服務將在 `http://localhost:8888` 上運行。您應該會看到類似以下的輸出：

```
Wahoo is running on port 8888...
```

## 專案結構

以下是本專案主要資料夾和檔案的結構與說明：

```
WaHoo/
├── AnswerFormatters/   # 各領域的答案生成與格式化模組
├── Architectures/      # 系統架構圖
├── Chatbot/            # 聊天機器人主邏輯
├── ContextManager/     # 上下文管理器
├── Dissection/         # 實體抽取引擎
├── Documentations/     # 專案相關文件
├── Engine/             # 整合所有模組的核心引擎
├── IntentClassifier/   # 意圖分類模型與預處理
├── IntentContent/      # 意圖相關的資料結構
├── IntentLoader/       # 意圖定義載入器
├── IntentSelector/     # 意圖選擇器
├── Preprocessor/       # 文本預處理工具 (如同義詞替換)
├── tests/              # 所有模組的單元測試
├── TornadoServer.py    # 主要的 Web 服務器入口
├── main.py             # 專案主程式 (備用執行入口)
├── config.py           # 專案設定檔
└── requirements.txt    # Python 相依套件列表
```

## API 使用方法

服務啟動後，您可以透過向 `/q` 端點發送 GET 請求來與引擎互動。

**請求格式**

```
GET /q?q=<您的查詢語句>
```

**範例**

您可以使用 `curl` 或任何程式語言來發送請求。

  - **查詢天氣**:

    ```bash
    curl "http://localhost:8888/q?q=台北今天天氣如何"
    ```

  - **播放音樂**:

    ```bash
    curl "http://localhost:8888/q?q=播放周杰倫的稻香"
    ```

  - **查詢股價**:

    ```bash
    curl "http://localhost:8888/q?q=台積電的股價"
    ```

**回傳格式**

伺服器會回傳一個 JSON 物件，其中包含生成的回答。

```json
{
  "answer": "正在為您查詢台北市今天的天氣...",
  "parameters": {
    "location": "臺北市",
    "datetime": "今天"
  },
  "intent": "Weather"
}
```

## 如何測試

本專案附有完整的單元測試，以確保各個模組的穩定性。您可以使用 `unittest` 來執行測試。

在專案根目錄下執行以下指令：

```bash
python -m unittest discover tests
```

這會自動發現並執行 `tests` 資料夾中的所有測試案例。

-----


### 整體意見

* **優點**：這份 `README.md` 結構清晰、內容完整，涵蓋了專案介紹、架構、功能、使用方式和測試等關鍵部分，能讓新的開發者或使用者快速上手。排版上使用了 Markdown 的標題、清單、程式碼區塊和引用，非常易於閱讀。
* **可加強部分**：
    * **授權條款 (License)**：建議在文件末尾新增一個「授權條款」部分，說明本專案遵循何種開源授權（例如 MIT, Apache 2.0 等），這對於開源專案來說非常重要。
    * **貢獻指南 (Contributing)**：如果這是一個希望社群參與的專案，可以新增一個 `CONTRIBUTING.md` 檔案，並在 README 中連結過去，說明如何提交問題 (Issue) 和拉取請求 (Pull Request)。

### 後續步驟

1.  **儲存檔案**：請將上述 Markdown 內容儲存到您專案的根目錄，並命名為 `README.md`。
2.  **檢視與調整**：您可以根據實際需求，微調文件中的細節。
3.  **新增其他文件**：考慮為您的專案新增 `LICENSE` 和 `CONTRIBUTING.md` 檔案。

如果您需要我針對特定部分做進一步的修改或補充，請隨時提出

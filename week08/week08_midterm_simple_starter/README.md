# 第 8 週學生起步專案（課堂簡化版）

先讀 [修訂版專題說明書](../生成式AI應用開發_第08週_期中個人小專題_課堂簡化版_專題說明書.md)。
這是可選用的起點，題目、輸入與欄位由學生自行設計；不用此骨架也可符合相同驗收標準。
教師範例提供完整流程供觀察，不可直接換標題後繳交。

## 安裝與啟動

在此 App 資料夾執行，本機授課 Python 3.14（本次實測 3.14.0）：

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
Copy-Item .env.example .env
python -m streamlit run app.py
```

macOS / Linux 使用 `python3.14 -m venv .venv`、`source .venv/bin/activate`、`cp .env.example .env`，其他指令相同。
`.env` 填入自己的 API key；Secrets > 環境變數（包含 .env，既有環境變數優先）。
缺少 Secrets 檔會回退至環境變數，設定內容不可顯示在畫面或截圖。
從課程根目錄啟動可用 `python -m streamlit run week08/week08_midterm_simple_starter/app.py`。

## 操作與資料流

app.py已依第7週格式加入教學重點、啟動說明、編號註解與分段空行。先定位A／B／C自己的設計，再沿「輸入→檢查→API→驗證→保存→顯示」閱讀；API關閉時只檢查設計，不產生模型成果。

1. 先不啟用 API，檢視介面。學生先完成 app.py 的 A／B／C 設計。
2. 輸入自己的虛構資料並送出：空白、超過 6000 字元、未完成設計會提示，0 次請求。
3. 基本檢查通過只代表輸入與規格可繼續，沒有模型輸出，也不是完整 JSON Schema 官方驗證器。
4. 設定金鑰、確認帳號可用且支援 Structured Outputs 的模型，再啟用 API 並送出。
5. 有效提交最多 1 次請求，SDK 不自動重試，網路等待設定 60 秒；再次送出另計。
6. 完成、非空、JSON 可解析、欄位合法後才保存。結果附原文，仍須人工查內容。
7. 一般重跑保留結果；切換 API 開關、按清除或再次送出會清掉前次結果。

app.py 按「設定→輸入→規格檢查→API→回應檢查→保存→顯示」閱讀。
只有兩個短函式：read_setting 讀設定，check_result 驗證字典欄位與型別。
本骨架只支援非空字串與非空字串組成的清單；清單允許空 list，不支援 enum、巢狀、nullable 或其他限制。
自行擴充型別時同步改 Schema、check_result、畫面與測試；不能只更動 Schema。
啟動／離線流程不會自動產生固定假摘要；真實成果必須自己操作並記錄。

## 學生改造與繳交

詳見說明書 A／B／C 規格；保留基本檢查與錯誤分流即可，不強制沿用函式名稱或此專案。
繳交前另寫自己的 README，使用 [專題設計與驗收紀錄](../第08週_課堂簡化版_專題設計與驗收紀錄.md)，不可直接交此教學說明。
若獨立成自己的 repository，請把上述相對文件連結改成自己的文件。

## Cloud部署（必做）與選做功能

第8週必須部署到Streamlit Community Cloud；驗收依[說明書第3-1節](../生成式AI應用開發_第08週_期中個人小專題_課堂簡化版_專題說明書.md)。老師須能開啟App網址，雲端介面可操作，並至少有一筆雲端真實API成功紀錄。
文字檔上傳、串流、聊天與JSON下載仍為選做。先完成最小任務與部署，延伸不得取代結構化輸出。
本版沒有檔案上傳與串流流程；可回查第 7 週簡化版的獨立範例。
Cloud 依平台可選 Python 版本另做部署驗證；本機使用 3.14 不代表雲端已驗證。整個課程 repo 的 Main file path 為 `week08/week08_midterm_simple_starter/app.py`，獨立 repo 則為 `app.py`。
平台 Secrets 參考 `.streamlit/secrets.example.toml`；真實金鑰檔不可提交。
把部署分支、入口、Cloud實際Python版本、App網址、老師觀看權限及驗收日期／結果寫入自己的README與驗收表。requirements須在入口同層或Repo根目錄，並已Push至部署分支。
正常／資訊不足兩筆可直接在雲端完成，不需本機再重做；若先前只有本機紀錄，補一筆雲端成功測試，追加請求另計。未部署或未通過須如實記錄並依公告期限補驗。
本次已在 Windows／Python 3.14.0 獨立環境安裝固定套件並通過 pip check、AppTest 與假 SDK 驗證；沒有執行真實 API、真人瀏覽器、Community Cloud 或課堂試教。

## 解譯器與版本重現

VS Code按Ctrl+Shift+P，選Python: Select Interpreter，指定此專案的`.venv/Scripts/python.exe`。
用 `python --version`、`python -m pip --version` 確認版本與路徑；系統Python與專案.venv的套件分開管理。
原本已有其他Python版本的.venv時，保留它，另建`.venv-py314`，上述指令中的環境名稱改成新名稱。
固定組合：Streamlit 1.63.0／OpenAI 2.49.0／python-dotenv 1.2.3。舊專案環境的1.60.0／1.2.2不會自動升級。
完整 Windows 間接依賴與安裝重現方式見[第7、8週Python3.14環境指南](../../docs/第07_08週_Python314環境指南.md)。
原Python3.12指南與快照保留作歷史比較，請勿用其constraints限制3.14環境。

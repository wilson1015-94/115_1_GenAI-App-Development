# 第 8 週學生起步專案｜Pydantic 課堂簡化版

先讀[專題說明書](../生成式AI應用開發_第08週_期中個人小專題_課堂簡化版_專題說明書.md)與[兩種版本對照](../第08週_課堂簡化版_JSON_Schema與Pydantic對照.md)。
本起點與 JSON Schema 版擇一即可，評分與驗收相同，不必完成兩版。
題目、使用者、欄位與介面由你設計；也可自行建立符合相同標準的 App。

## 安裝與啟動

在本資料夾執行，使用 Python 3.14：

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
Copy-Item .env.example .env
python -m streamlit run app.py
```

macOS／Linux 改用 `python3.14 -m venv .venv`、`source .venv/bin/activate`、`cp .env.example .env`；尚未在這兩個平台實測。
VS Code 的 Python: Select Interpreter 須選本資料夾的 `.venv/Scripts/python.exe`，並核對 `python --version` 與 `python -m pip --version`。
已有其他虛擬環境時先保留，另建 `.venv-py314`，以上啟動路徑一起調整。
從課程根目錄可執行 `python -m streamlit run week08/week08_midterm_simple_pydantic_starter/app.py`。

`.env` 填自己的金鑰；Secrets 優先於環境變數（`.env` 不覆寫既有環境變數）。
參考 `.streamlit/secrets.example.toml`，不要提交真正的 `.env` 或 `secrets.toml`。
本版直接依賴：OpenAI 2.49.0、Streamlit 1.63.0、python-dotenv 1.2.3、Pydantic 2.14.1。
完整快照、constraints 安裝方式與雲端限制見[環境指南](../../docs/第07_08週_Python314環境指南.md)。

## 先完成 A／B／C，再開啟 API

| 任務 | 修改位置 | 完成條件 |
|---|---|---|
| A：定位與規則 | `APP_TITLE`、`INSTRUCTIONS` | 清楚的使用者與任務、只依原文、資訊不足處理 |
| B：資料契約 | `class ProjectResult` | 自訂至少兩個有用途的必填欄位，使用 `str` 或 `list[str]`，保留 `extra="forbid"` 與 `strict=True` |
| C：介面 | `FIELD_LABELS`、表單與結果區 | 標籤對應自己的欄位，使用者能對照原文閱讀結果 |

學生模型刻意沒有欄位，尚未完成時會在請求前停止；不需要先填入教師摘要器的答案。
欄位可用 `Field(description="欄位用途")` 補充說明；本起點不用預設值，表示每欄必填。
若需要數字、nullable、enum 或巢狀模型，請同步擴充設計檢查、驗證與顯示；這些不是最低要求。

## 程式讀法與觀察

沿編號閱讀「輸入→模型規格→API→檢查→保存→顯示」。只有模型類別與兩個短函式，沒有跨檔 helper。

1. 預設 API 關閉，初啟動與離線操作都是 0 次請求；不會產生固定假摘要。
2. 空白、超過 6000 字元、未完成設計或缺金鑰，皆在送出請求前停止。
3. `model_fields` 只讀本機規格；離線通過不代表真實模型成果或伺服器接受所有擴充規格。
4. 啟用後，每次有效提交以 `responses.parse(text_format=ProjectResult)` 最多請求一次。SDK 不重試，網路等待設定 60 秒，`store=False` 仍會傳送原文並可能計費。
5. SDK 把模型轉成 strict JSON Schema，並嘗試解析與驗證回應。JSON 或型別不合格可能在 `parse()` 內先拋出 `ValidationError`，因此不保證先取得 response 才報錯。
6. 回應取得後仍檢查拒答、完成狀態與非空文字，再取 `output_parsed`；沒有解析物件不能當成成功。
7. `result` 是 Pydantic 物件，`model_dump()` 轉成 `data` 字典；`check_result` 再拒絕空白文字。文字清單可為空，每個既有項目須有內容。
8. 全部通過才保存 `st.session_state.record`（原文＋data）。一般 rerun 保留結果；清除、切換模式或新提交失敗會清掉舊成果。

模型的 `ConfigDict(strict=True)` 控制本機型別驗證；API 的 strict Schema 由 SDK 產生，兩者分工不同。
格式與型別合法仍不保證內容正確，請回看原文；`model_dump()` 也不代表資料已寫入檔案。

## 驗收、繳交與延伸

沿用同一份[設計與驗收紀錄](../第08週_課堂簡化版_專題設計與驗收紀錄.md)：至少保留正常、資訊不足各一筆真實 API 紀錄，逐欄查原文；學生規劃共 2 次，額外修正另計。
README 說明採用 Pydantic 的理由、自己的欄位與限制、實際版本及實測／未測項目。不可直接交本教學 README，也不可只換教師範例名稱。
未完成真實測試就填未測，假回應不算成果。上傳、串流與聊天仍為選做；Cloud部署為必做。

## Cloud部署（必做）

第8週必須部署到Streamlit Community Cloud；驗收依[說明書第3-1節](../生成式AI應用開發_第08週_期中個人小專題_課堂簡化版_專題說明書.md)。老師須能開啟App網址，雲端介面可操作，並至少有一筆雲端真實API成功紀錄。
Cloud 的入口依 Repo 結構選 `week08/week08_midterm_simple_pydantic_starter/app.py` 或獨立 Repo 的 `app.py`；確認部署分支的入口、套件清單與 Secrets。
requirements須在入口同層或Repo根目錄，包含Pydantic且已Push；設定依 `.streamlit/secrets.example.toml` 放平台Secrets，Cloud Python須按平台選項與實測確認。
自己的README與驗收表必填App網址、分支／入口、Cloud實際Python版本、老師觀看權限、驗收日期與結果。
正常／資訊不足兩筆可直接在雲端完成，不需本機再重做；若先前只有本機紀錄，補一筆雲端成功測試並記錄追加請求。未部署或未通過須如實記錄並依公告期限補驗。
複製到自己的學期 Repo 時，依[Git 通用指南](../../week07/生成式AI應用開發_第07週_Git實作教材_學期共用Repo版.md)調整路徑與清單，不要直接覆蓋既有套件清單。

教師離線檢查：`python -X utf8 scripts/verify_week08_pydantic.py`（由課程根目錄執行）。
此檢查使用 AppTest 與模擬 HTTP，沒有付費 API 請求，不代表真人瀏覽器、Cloud、Colab 或課堂試教通過。
2026-10-28 已在既有 Windows／CPython 3.14.0 固定環境通過檢查與 pip check：Streamlit 1.63.0、OpenAI 2.49.0、Pydantic 2.14.1、python-dotenv 1.2.3；本次未重新安裝或升級套件。

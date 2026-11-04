# 第 8 週教師完整摘要器｜Pydantic 課堂簡化版

先讀[專題說明書](../生成式AI應用開發_第08週_期中個人小專題_課堂簡化版_專題說明書.md)與[兩種版本對照](../第08週_課堂簡化版_JSON_Schema與Pydantic對照.md)。
本例與[JSON Schema 教師版](../week08_midterm_simple_teacher/README.md)使用相同名稱、任務規則、文字輸入、`title`／`summary`／`key_points` 與畫面標籤。
學生擇一採用起點即可；教師範例示範完成度，不能直接換名稱繳交。

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
VS Code 的 Python: Select Interpreter 須選本資料夾的 `.venv/Scripts/python.exe`；用 `python --version` 與 `python -m pip --version` 核對。
已有其他環境先保留，另建 `.venv-py314` 並調整啟動路徑。
從課程根目錄可執行 `python -m streamlit run week08/week08_midterm_simple_pydantic_teacher/app.py`。

Secrets 優先於環境變數；本機 `.env` 不覆寫既有環境變數。設定範本為 `.env.example` 與 `.streamlit/secrets.example.toml`，真正的金鑰檔不可提交。
直接依賴為 OpenAI 2.49.0、Streamlit 1.63.0、python-dotenv 1.2.3、Pydantic 2.14.1；完整快照與 constraints 見[環境指南](../../docs/第07_08週_Python314環境指南.md)。

## 完整示範與預期觀察

1. API 保持關閉，輸入「社團下週舉辦讀書交流，報名方式尚未決定。」並送出。應提示基本檢查通過，沒有摘要與 API 請求。
2. 空白或 6001 字元應在本機停止。設定金鑰與帳號可用模型後，才啟用 API，使用同一筆文字示範一次；不要為比較兩版而要求每位學生重複付費。
3. 預期三欄型別正確，`title`／`summary` 與每個重點不能全空白；`key_points=[]` 合法。內容與措辭不保證兩版相同，也沒有唯一標準答案。
4. 人工確認沒有補造日期、人物或報名方式。一般 rerun 保留當筆原文與結果；清除、切換模式或再送出失敗須清掉舊成果。

課堂沿編號說明：`ProjectResult` 定義規格→`responses.parse(text_format=ProjectResult)` 發出請求→SDK 解析與驗證→App 檢查拒答／完成／非空／解析物件→`model_dump()` 轉 dict→補查空白→成功保存與顯示。
SDK 可能在 `parse()` 內就因 JSON 或欄位型別不合格拋出 `ValidationError`，下方捕捉並顯示簡短錯誤，不顯示帶原始資料的完整例外。
未完成、拒答、空回應、缺少解析物件與驗證失敗都不得保存。

## 模型與兩個短函式的分工

| 位置 | 責任 |
|---|---|
| `ProjectResult` | 三個必填欄位；`extra="forbid"` 拒絕多欄，`strict=True` 拒絕型別轉換 |
| `read_setting` | 讀取 Secrets／環境變數 |
| `check_result` | Pydantic 通過後補查空白字串，允許空清單 |
| `model_dump()` | 將已驗證物件轉成字典，交給相同的狀態與顯示流程 |

本機 `strict=True` 與 SDK 產生的 API strict Schema 是兩個層次；格式合格仍須人工查原文。
程式保留教師提醒，指認學生 A／B／C 的個人設計位置。學生不必使用這三欄或這個題目；起點支援必填 `str` 與 `list[str]`，其他型別須同步擴充設計檢查、驗證與顯示。

## 相同驗收與請求數

沿用[設計與驗收紀錄](../第08週_課堂簡化版_專題設計與驗收紀錄.md)與原評分比例，Pydantic 不加分也不提高最低門檻。
預設關閉，初啟動／離線 0 次；有效提交最多 1 次，`max_retries=0`、`timeout=60`、`store=False`。教師規劃 1 次示範，學生正常與資訊不足各 1 次共 2 次；額外測試另計，失敗也可能計費。
金鑰、網路或模型排障超時，先完成離線設計，真實成果明列待補驗。

教師檢查從課程根目錄執行：

```powershell
python -X utf8 scripts/verify_week08_simple.py
python -X utf8 scripts/verify_week08_pydantic.py
```

新檢查用真實 OpenAI SDK 搭配 `httpx.MockTransport`，驗證送出的 strict Schema 與真實 Pydantic 解析；HTTP 完全模擬，不會連到 OpenAI。
同一組成功／失敗資料用於兩種教師版與填妥設計的學生版，另查未完成設計零請求與學生自訂欄位。
離線通過不代表真實模型品質、真人瀏覽器、Cloud、Colab、其他平台或課堂時間已驗證。
2026-10-28 已在既有 Windows／CPython 3.14.0 固定環境通過兩支驗證與 pip check：Streamlit 1.63.0、OpenAI 2.49.0、Pydantic 2.14.1、python-dotenv 1.2.3。本次未重新安裝或升級套件。

## Cloud部署（必做）

第8週必須部署到Streamlit Community Cloud；驗收依[說明書第3-1節](../生成式AI應用開發_第08週_期中個人小專題_課堂簡化版_專題說明書.md)。老師須能開啟App網址，雲端介面可操作，並至少有一筆雲端真實API成功紀錄。
入口為 `week08/week08_midterm_simple_pydantic_teacher/app.py`，獨立 Repo 則為 `app.py`；requirements須在入口同層或Repo根目錄，包含Pydantic且已Push至部署分支。
依 `.streamlit/secrets.example.toml` 設定平台Secrets，Cloud Python按平台選項與實測確認；自己的README與驗收表必填App網址、分支／入口、Cloud實際Python版本、老師觀看權限、驗收日期與結果。
正常／資訊不足兩筆可直接在雲端完成，不需本機再重做；若先前只有本機紀錄，補一筆雲端成功測試並記錄追加請求。未部署或未通過須如實記錄並依公告期限補驗。
若改成自己的Repo，請調整README內連結。上傳、串流與聊天仍為選做。

API 寫法依[OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses)，模型／字典分工依[Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)。

# 第11週｜RAG文件問答・修訂版App

流程：**找證據 → A組成context → 交給模型回答 → 核對來源**。本週只做自行建置的RAG。
搭配上層檔名含「RAG文件問答_課堂簡化版_修訂版」的學生／教師Notebook。原課堂簡化版（`week11_rag_simple/`）保留未改。

**第9～11週整合示範：**另有[完整上傳與RAG App](../week11_rag_integrated_revised/README.md)，可逐步查看文件抽取、清理、切塊、文件／問題向量、排名、context與回答。操作見[學生講義](../第11週_第09至11週整合RAG_App_操作與觀察講義_修訂版.md)；完整示範不增加必做TODO，本資料夾的A與作業要求維持原樣。

## 學生操作

1. 開啟學生Notebook，完成A的`build_context`並通過自我檢查。
2. 把同一個函式貼到`student/app.py`的同名函式；其他函式與畫面都已提供。
3. 先用預設的**離線模式**（0次API）：App用第10週的關鍵字規則找證據、A組context，並在「送出前預覽」顯示模型會收到的內容。離線不會產生回答。
4. 有金鑰後勾選「使用真實API」，問正常、資訊不足、文件外三種問題，各下載一份問答紀錄，再回原文核對。沒有API時，真實欄寫「未測」，或引用老師的實測紀錄（要標明來源）。

## 資料：直接接第10週

- 預設文字`sample_data/week09_cleaned_text.txt`與第10週修訂版完全相同（第9週`sample.txt`清理後的3段）。
- `sample_data/questions.json`是第10週同樣的4題（原句、改寫、資訊未提供、文件外），另加「好的回答應該」。
- 作業時把自己的文件貼進文件欄即可（空白行分段）。

## 安裝與啟動

沿用Windows／Python 3.14；直接依賴版本在`requirements.txt`。既有環境先確認，不要覆蓋原本的`.venv`。

```powershell
cd week11/week11_rag_revised
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run student/app.py
```

- 教師版改成`teacher/app.py`。從Repo根目錄啟動也可以；範例檔與`.env`依App位置讀取。
- 部署是選做，步驟沿用[第7週起Git指南](../../week07/生成式AI應用開發_第07週_Git實作教材_學期共用Repo版.md)。Colab只執行Notebook，不架Streamlit。

## 金鑰：本機、Streamlit Cloud與Colab都能執行

App用`read_setting`讀設定：**平台Secrets優先，沒有時讀環境變數；`.env`在啟動時載入**。同一份程式不用改，本機與Cloud都能跑。

| 執行位置 | 金鑰放哪裡 | 說明 |
|---|---|---|
| 本機App與Notebook | 本資料夾的`.env`（由`.env.example`複製） | 學生版、教師版與Notebook共用。也可放`student/`或`teacher/`的`.env`；兩處都有時以本資料夾的為準 |
| Streamlit Cloud | App設定的**Secrets** | 格式見`student/.streamlit/secrets.example.toml` |
| Colab Notebook | Colab的Secrets，並授權Notebook | 只跑Notebook |

部署到Streamlit Community Cloud時：Main file path填`week11/week11_rag_revised/student/app.py`（依自己Repo的實際路徑）；入口同層已附`requirements.txt`；在Advanced settings → Secrets貼上：

```toml
OPENAI_API_KEY = "你的金鑰"
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
```

真正的`.env`與`secrets.toml`都不要提交到GitHub。

## App怎麼運作

| 模式 | 做什麼 | 請求次數 |
|---|---|---|
| 離線（預設） | 第10週關鍵字規則找證據 → A組context → 顯示送出前預覽 | 0次 |
| 真實API | 文件各段與問題1次Embedding → `rank_chunks`排名 → A組context → 1次Responses；沒有證據時直接回不足句，不呼叫模型 | 每題最多2次 |

- 規則放instructions，問題與context放input；答案要標`[來源n]`。
- 回答回來用`check_answer`核對：有標來源、承認資訊不足、引用了不存在的來源、沒有標來源四種判斷。這只看格式，內容仍要回原文確認。
- 按「找證據並回答」才處理；每次送出先清掉舊結果，失敗時畫面顯示錯誤、不留舊答案。重跑畫面或下載不會再呼叫API。
- A還沒完成時，App會停在第一步，不送付費請求。
- 下載的`rag_record.json`含模式、問題、參數、取回片段、context、回答與核對結果；不含金鑰或向量。
- 下載後把`rag_record.json`放到Notebook所在的資料夾（Colab拖進左側「檔案」窗格），執行10-1讀回格：檢查context裡每個`[來源n]`都是取回的證據原文。第二份起檔名若是`rag_record (1).json`，改格內的path。0次API。

為了讓流程簡單直線，每次送出都重新向量化文件；正式服務會保存文件向量，查詢時只向量化新問題。

## 教師實測紀錄（給沒有API的同學）

老師課前在Notebook第7-1節開啟`RUN_REAL_RAG`實跑，再開啟第8節的`SAVE_TEACHER_RECORD`，會在Notebook資料夾存下`teacher_rag_record.json`（日期、模型、每題的片段、回答與核對結果，不含金鑰與向量）。把這個檔案發給學生，放在Notebook所在資料夾即可讀取。學生在B表要標明「教師實測紀錄」。本資料夾不附這個檔案，因為它必須是真實執行的結果。

## 練習與作業

- A是唯一的程式實作；B是四種問題的人工判讀（檢索問題、生成問題、引用不支持、合理的資訊不足）。
- 課後45～60分鐘：換一份合法小文件；交學生Notebook、App、原文件、三份問答紀錄JSON與README。**不交金鑰或`.env`**。三題最多6次API。
- 評量40／30／20／10：A與來源、B與回答、錯誤修正、可重現與反思。不需要部署或向量資料庫。

## 重建與驗證

教師重建與檢查（Repo根目錄）：

```powershell
python -X utf8 scripts/build_week11_revised.py
python -X utf8 scripts/verify_week11_revised.py
```

重建會讀取第10週修訂版的資料、問題與三個函式，產生雙版Notebook／Markdown、雙版App、範例資料與設定範本；不覆蓋本README與教師導讀，也不呼叫API。已測與未測範圍見[教師導讀](../第11週_課堂簡化版修訂版_教師導讀與修訂紀錄.md)。

OpenAI代管的File Search只在Notebook第12節做概念比較，本App不包含。官方說明：[Retrieval](https://developers.openai.com/api/docs/guides/retrieval)、[Responses](https://developers.openai.com/api/docs/guides/text)、[File Search](https://developers.openai.com/api/docs/guides/tools-file-search)。

# 第10週｜Embedding與語意搜尋・修訂版App

從第9週已確認的文字出發，只做「片段 → 向量 → 相似度 → 找出片段 → 回到原文確認」，不產生回答。
搭配上層檔名含「課堂簡化版_修訂版」的學生／教師Notebook。原課堂簡化版（`week10_semantic_search_simple/`）保留未改。

## 學生操作

1. 開啟學生Notebook，看完cosine示範後完成A（計分、來源複製、篩選、排序與top_k），並通過自我檢查。
2. 把同一個`rank_chunks`貼到`student/app.py`的同名函式；其他函式與畫面已完整提供，不必再寫。
3. 先用預設的離線規則跑通流程。它是人工關鍵字計數，不是語意模型：用字不同的改寫問題可能找不到，這正是要觀察的限制。
4. 設好金鑰後可勾選真實模式，比較原句、改寫、資訊未提供、文件外四種問題。沒有API時，真實語意欄寫「未測」，或引用老師的實測紀錄（要標明來源）。
5. 固定同一題，只改top_k或最低分數做兩組比較，回到原文核對並下載搜尋紀錄；改滑桿與下載都不會再呼叫API。

## 資料：直接接第9週

- 預設文字`sample_data/week09_cleaned_text.txt`＝第9週`sample.txt`清理後的結果（與第9週修訂版App「下載清理後文字」相同），空白行分成3段。
- 也可以貼上自己第9週App下載的`cleaned_text.txt`。若是CSV清理後的文字，列與列之間要加空白行，每一列才會各成一段。
- 範例問題在`sample_data/questions.json`：原句、改寫、資訊未提供、文件外各一題，附預期片段；Notebook用的是同一組問題。

## 安裝與啟動

沿用Windows／Python 3.14；直接依賴版本在`requirements.txt`。既有環境先確認，不要覆蓋原本的`.venv`。

```powershell
cd week10/week10_semantic_search_revised
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m streamlit run student/app.py
```

- 教師版改成`teacher/app.py`。也可從Repo根目錄啟動`python -m streamlit run week10/week10_semantic_search_revised/student/app.py`；範例檔依App位置讀取，不受目前目錄影響。
- 部署是選做，步驟沿用[第7週起Git指南](../../week07/生成式AI應用開發_第07週_Git實作教材_學期共用Repo版.md)。Colab只執行Notebook，不架Streamlit。

## 金鑰：本機、Streamlit Cloud與Colab都能執行

App用`read_setting`讀設定：**平台Secrets優先，沒有時讀環境變數或本資料夾的`.env`**。所以同一份程式不用改，本機與Cloud都能跑。

| 執行位置 | 金鑰放哪裡 | 說明 |
|---|---|---|
| 本機App | 本資料夾的`.env`（由`.env.example`複製） | 學生版、教師版與Notebook共用；也可放`student/`或`teacher/`的`.env`，或用環境變數 |
| 本機Notebook | 同上 | 先讀`week10_semantic_search_revised/.env`，再找Notebook所在資料夾往上的`.env` |
| Streamlit Cloud | App設定的**Secrets** | 格式見`student/.streamlit/secrets.example.toml`，寫在最外層，不加區段標題 |
| Colab Notebook | Colab的Secrets，並授權Notebook | 只跑Notebook，不架Streamlit |

部署到Streamlit Community Cloud時：
1. **Main file path**填`week10/week10_semantic_search_revised/student/app.py`（依自己Repo的實際路徑）。
2. 入口同層已附`requirements.txt`；Cloud先找入口同層，再找Repo根目錄，不會往上一層找。
3. 在Advanced settings → Secrets貼上：

```toml
OPENAI_API_KEY = "你的金鑰"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
```

範例文字依App位置讀取，Cloud也讀得到。真正的`.env`與`secrets.toml`不要提交到GitHub。

## 範圍與API次數

- 文件最多6000字元、12段、每段1000字元；問題最多300字元。超過就拒絕，不會截斷原文。
- 每個片段保留`chunk_id/source/start/end/text`，且`text == 貼入文字[start:end]`。
- 預設離線0次API；真實模式每次有效提交最多1次`embeddings.create`（文件片段與問題合成一批）。A未完成、輸入不合格或缺金鑰時0次。
- Notebook教師示範1次（3段文件＋4個問題）；學生App三種問題各1次，共3次。改滑桿、清除、下載與一般rerun都是0次；新提交與額外重測另計。
- 為了讓流程簡單直線，每次新提交都重新向量化文件；正式服務應保存文件向量，查詢時只向量化新問題。
- 文件與問題用同一個模型；離線規則與真實向量不可混用。回傳依index對齊，筆數、維度、非有限數字或全零向量不合格就不保存。
- SDK自動重試關閉，每次網路等待60秒，不代表整個任務60秒內完成。Embeddings仍會把文字送到OpenAI。

## 畫面與成功資料

- 按「建立向量並搜尋」才處理。新提交先清掉舊結果；輸入、A、API與向量檢查都通過才保存原文、問題、模式、模型與向量。失敗、切換模式或按清除都會移除結果。
- top_k與門檻滑桿在表單外，只用已保存的向量重排。分數不是正確機率：高分可能沒有證據，門檻太高可能排掉相關片段，規則全零時回傳空結果。
- 下載的`search_record.json`含模式、模型、問題、原文、參數與排名，不含金鑰與整批向量；空結果也可以下載。下載後仍要回原文核對，不能只看分數。
- 下載後把`search_record.json`放到Notebook所在的資料夾（Colab拖進左側「檔案」窗格），執行9-1讀回格：檢查片段等於`source[start:end]`、分數排序、門檻與top_k。第二份檔名若是`search_record (1).json`，改格內的path。0次API。

## 教師實測紀錄（給沒有API的同學）

老師課前在Notebook第7節開啟`RUN_REAL_EMBEDDINGS`與`SAVE_TEACHER_RECORD`，會存下`teacher_ranking_record.json`（含日期、模型與排名，不含向量）。
把這個檔案發給學生，放在Notebook所在資料夾，7-2節就能讀出真實Embedding的排名。學生在B表要標明「教師實測紀錄」，不能寫成自己執行的結果。本資料夾不附這個檔案，因為它必須是真實執行的結果。

## 練習與作業

- A是唯一的程式實作；B是同一份資料的四種問題與兩組參數觀察。核心150分鐘＋休息10分鐘＋排障20分鐘；課後45～60分鐘換一份合法小文件，沿用同一個App。
- 交學生Notebook、同一個App、原文件或貼入文字、兩份搜尋紀錄JSON與README。README至少記：模式與實際版本、三類問題的預期與實際片段、兩組參數比較、一個證據不足、一個錯誤或邊界的處理與重測、一個日期或數字的人工核對、API次數與未測項目。
- 評量40／30／20／10：A功能與來源、B比較與判讀、錯誤修正、可重現與反思。沿用整學期Repo與既有表單，不另交每週資料夾連結。教師答案不隨學生包發放。

## 第11週銜接與驗證

本週用普通list理解文件向量、問題向量與排名；第11週才把找到的片段組成context並產生回答，另一路是OpenAI File Search由平台代管切塊、向量化與檢索。兩條路線都要核對原文。本週不建立平台資源，不需要ChromaDB／FAISS；有餘裕可回看[原第10週向量資料庫說明](../week10_semantic_search_app/README.md)。

教師重建與檢查（Repo根目錄）：

```powershell
python -X utf8 scripts/build_week10_revised.py
python -X utf8 scripts/verify_week10_revised.py
```

重建會產生雙版Notebook／Markdown、雙版App、範例資料與設定範本，不覆蓋本README與教師導讀。已測／未測範圍見[教師導讀](../第10週_課堂簡化版修訂版_教師導讀與修訂紀錄.md)。

官方說明：[OpenAI Embeddings](https://developers.openai.com/api/docs/guides/embeddings)、[Create embeddings](https://developers.openai.com/api/reference/resources/embeddings/methods/create)、[Retrieval](https://developers.openai.com/api/docs/guides/retrieval)。

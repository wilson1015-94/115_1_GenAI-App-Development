# 第9週文件處理｜修訂版App

本App的流程：**讀取 → 清理 → 切塊 → 檢查 → 匯出**，為第10週語意搜尋與第11週RAG準備資料。
搭配上層檔名含「課堂簡化版_修訂版」的學生／教師Notebook。原課堂簡化版（`week09_document_simple/`）與原範例資料夾`sample_tata/`保留未改。

## 學生從這裡開始

1. 在Notebook看完短示範，完成引導練習A（清理）並通過自我檢查；活動B用已提供的切塊函式比較兩組參數，填寫觀察表。
2. 只把完成的`clean_text`貼到`student/app.py`的同名函式（保留`import re`）。讀取、切塊與畫面都已提供。
3. 啟動App，資料來源選「內建範例」：先跑`sample.txt`，再換`sample.csv`、`sample.pdf`、`sample.docx`。A未完成時會顯示提示，不會有假的成功結果。
4. 固定同一份文件與chunk_size，只改overlap；下載兩份JSON讀回，挑一個問題找出支持答案的片段與原文，核對日期或數字。
5. 作業沿用同一個App換一份文件；並下載「清理後文字」保留給第10週使用。完整規格與評分在Notebook第7節。

教師使用`teacher/app.py`；請勿把教師程式或教師Notebook放進學生發放資料。

## 範例檔（Notebook與App共用）

四個範例都在[sample_data](sample_data/README.md)：`sample.txt`、`sample.csv`、`sample.pdf`、`sample.docx`，皆為虛構活動資料。

- **App：**資料來源選「內建範例」，從下拉選單選檔即可，不必上傳。
- **Notebook：**先把這四個檔案複製到Notebook所在的資料夾（`week09/`）；Colab直接上傳。範例程式只寫檔名。
- Notebook第6節與App選`sample.txt`、size=120、overlap=20時，結果應該相同。

## Windows／Python 3.14安裝與啟動

在課程Repo根目錄先進入本資料夾：

```powershell
cd week09/week09_document_revised
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install -r requirements.txt
python -m pip check
python -m streamlit run student/app.py
```

- 已有`.venv`時先確認版本；不要覆蓋原環境，可改建`.venv-py314`。VS Code請選取該環境的`Scripts/python.exe`，安裝與啟動要用同一個環境。
- 若PowerShell阻擋啟用指令，可直接使用`.\.venv\Scripts\python.exe -m pip ...`與`.\.venv\Scripts\python.exe -m streamlit run student/app.py`。
- 教師版：`python -m streamlit run teacher/app.py`。也可以從Repo根目錄執行`python -m streamlit run week09/week09_document_revised/student/app.py`；範例檔依程式位置讀取，不受目前目錄影響。
- Colab只執行Notebook短例子，不開Streamlit。部署是選做，共通操作見[第7週起Git指南](../../week07/生成式AI應用開發_第07週_Git實作教材_學期共用Repo版.md)。

## 檔案與責任

| 檔案 | 內容 |
|---|---|
| `student/app.py` | 學生A清理骨架；完整切塊、讀取與畫面 |
| `teacher/app.py` | 相同流程的完整參考答案 |
| `sample_data/` | 與Notebook相同的四個範例檔 |
| `requirements.txt` | App與PDF／Word讀取套件 |
| `requirements-api.txt` | 只有Notebook選做AI摘要需要 |
| `.gitignore` | 排除環境、快取與真實金鑰設定 |

## 操作規格

App沒有API功能，全程0次請求，不需要`.env`或Secrets。資料來源、編碼與參數都在表單裡，按「處理文件」才讀取；改了值但沒按，畫面仍標示為上次成功結果。

- 新提交先清掉舊結果，全部通過才保存。按清除、A未完成、空白檔、解碼錯誤、檔案損壞或參數不合理，都不會留下舊的下載。
- 預覽片段或下載只使用已保存的資料，不重新讀檔。

| 限制 | 處理方式 |
|---|---|
| 檔案1MB、PDF50頁、CSV200列 | 超過就拒絕，不會偷偷截斷 |
| 清理後1～20000字元 | 超過或沒有內容就拒絕 |
| TXT／MD／CSV編碼 | 上傳檔案預設UTF-8-SIG，可選CP950；不自動猜測、不忽略錯誤。內建範例固定UTF-8 |
| CSV | 逗號分隔，保留欄名與每一列；空欄名、重複欄名或欄數不合會被拒絕 |
| PDF | 讀文字層；全部沒有文字時提示可能需要OCR，部分無文字頁保留頁碼與提示 |
| Word | 依本文順序讀段落與表格；不保證圖片、巢狀表格、頁首頁尾完整 |
| 片段位置 | `text == cleaned_text[start:end]`；end不包含，位置不是PDF座標 |

以上是課堂小文件的範圍，不是公開服務的完整防護。讀取成功後，仍要對照原檔核對日期、數字與順序。

## 兩種下載

| 下載 | 內容 | 用途 |
|---|---|---|
| `document.chunks.json` | filename、encoding、character_count、chunk_size、overlap、raw_text、cleaned_text、chunks（每個含chunk_id、start、end、text） | 本週作業：比較兩組參數、讀回驗證start:end |
| `cleaned_text.txt` | 清理後文字（段落以空白行分隔） | 第10週：貼進語意搜尋App的文字框，以空白行分段 |

第10週App不會匯入JSON；請一併保留原文件與清理後文字。CSV清理後每列之間沒有空白行，若想讓每一列各成一段，貼入前在列與列之間加空白行。

## 練習、作業與繳交

- 核心150分鐘，另留休息10分鐘與排障20分鐘。A是清理實作，B是參數比較與來源判讀；App只需放入A。
- 回家作業45～60分鐘：交同一個App、完成A與B紀錄的學生Notebook、原文件、兩份JSON、清理後文字與README；不另做第二個App或手寫切塊。
- README至少寫：用途與來源、啟動方式與實際版本、兩組參數與邊界實例、一個問題及兩組支持答案的chunk_id與原文、一個錯誤或邊界與處理、核對的日期或數字、限制與未測項目。
- 推送到整學期自己的Repo；老師從既有表單登記的Repo查看，不另交每週資料夾連結。

## 選做摘要

Notebook第9節自帶短文字，預設`RUN_PAID_API=False`（0次）；基本作業不需要開啟。

```powershell
python -m pip install -r requirements-api.txt
```

金鑰只放在環境變數或自己的`.env`；Colab使用Secrets並授權Notebook。不要上傳真實金鑰、`.env`或`secrets.toml`。
每次有效執行最多1次請求、關閉自動重試、最多6000字元、不截斷。`store=False`不代表資料留在本機；模型可用性與品質需課前用教學帳號確認。

## 第10、11週銜接

- 第10週：把確認過的清理後文字貼進語意搜尋App（以空白行分段，最多12段）。
- 第11週：自行建置RAG或OpenAI File Search擇一。File Search由平台處理支援文件的切塊、向量化與索引；需要上傳文件，有格式與費用條件，不保證CSV可直接上傳。
- 兩條路線都要求核對原文與來源；本週不建立任何平台資源。官方依據：[OpenAI Retrieval](https://developers.openai.com/api/docs/guides/retrieval)、[File Search](https://developers.openai.com/api/docs/guides/tools-file-search)。

## 教師重建與驗證

在課程Repo根目錄、啟用已安裝套件的環境後執行：

```powershell
python -X utf8 scripts/build_week09_revised.py
python -X utf8 scripts/verify_week09_revised.py
```

重建會產生兩份Notebook／Markdown、兩份App、requirements與`.gitignore`，並從`week09/sample_tata/`複製四個範例檔到`sample_data/`；本README、`sample_data/README.md`與教師導讀不會被覆蓋。
驗證結果與未測項目見[教師導讀](../第09週_課堂簡化版修訂版_教師導讀與修訂紀錄.md)；離線檢查與AppTest不等於真人瀏覽器、API、Colab、Cloud或試教通過。

# 第 11 週作業｜RAG 文件問答與第 9～11 週整合實作紀錄

## 1. 環境版本與執行模式
- **作業作者**：李承威
- **Python 與套件實際版本**：Python `3.14.0`、Streamlit `1.63.0`、OpenAI SDK `2.49.0`、python-dotenv `1.2.3`、pypdf `6.18.1`、python-docx `1.2.0`
- **執行模式與模型**：
  - 向量檢索模型：`text-embedding-3-small`（真實 Embeddings API）
  - 回答生成模型：`gpt-5.4-mini`（真實 Responses API，`store=False, max_retries=0, timeout=60.0`）
- **啟動方式**：
  ```zsh
  # 啟動第 11 週練習版 App（對應 10-1 與第 11 節回家作業）
  cd week11/week11_rag_revised
  python -m streamlit run student/app.py

  # 啟動第 9～11 週整合版 RAG App（對應 10-2 檢查）
  cd week11/week11_rag_integrated_revised
  python -m streamlit run app.py
  ```

---

## 2. 第 11 節回家作業：自己的文件三類問題與 10-1 讀回驗證

使用自訂虛構文件 [cleaned_text.txt](cleaned_text.txt)（「校園AI創新黑客松競賽辦法」，共 4 段，`chunk 0`～`chunk 3`），在練習版 App（[week11_rag_revised/student/app.py](week11_rag_revised/student/app.py)）以真實 API 測試三種問題並下載三份問答紀錄，全數通過 Notebook **第 10-1 節**讀回檢查：

| 問題類型與紀錄檔 | 取回並放進 `context` 的來源片段 | 模型實際回答與 `check_answer` 結果 | 原文核對與檢索／生成判讀 |
| --- | --- | --- | --- |
| **1. 正常題**：`活動地點在哪裡？`<br>（[rag_record.json](rag_record.json)） | • `[來源1]` `chunk 3`（分數 `0.4159`）<br>• `[來源2]` `chunk 0`（分數 `0.3882`） | 回答：「**活動地點在資訊大樓三樓創客空間。[來源2]**」<br>核對：`有標來源：請回原文核對` | **引用與原文完全相符**：檢索階段因 `chunk 3` 含「活動當日」而排第 1、真正含舉辦地點的 `chunk 0` 排第 2；幸好 `top_k=2` 將兩段皆放入 `context`，生成模型精準辨識並標註 `[來源2]`（對應 `chunk 0`：「競賽日期為2026年12月15日，時間為上午9點至下午5點，舉辦地點在資訊大樓三樓創客空間。」）。 |
| **2. 資訊不足題**：`交通補助與住宿怎麼申請？`<br>（[rag_record-2.json](rag_record-2.json)） | • `[來源1]` `chunk 3`（分數 `0.5255`） | 回答：「**根據目前文件，無法確認這個問題。**」<br>核對：`承認資訊不足` | **正確承認資訊不足**：檢索成功取回 `chunk 3`（原文明確寫「交通補助與住宿安排尚未提供，請參賽者自行處理。」），生成模型未自行編造申請流程，依規則回答無法確認。 |
| **3. 文件外題**：`學校圖書館幾點開放？`<br>（[rag_record-3.json](rag_record-3.json)） | • `[來源1]` `chunk 0`（分數 `0.2619`） | 回答：「**根據目前文件，無法確認這個問題。**」<br>核對：`承認資訊不足` | **正確攔截文件外問題**：雖然 `chunk 0` 分數 `0.2619` 略高於預設門檻而進入 `context`，但原文僅提黑客松時間地點、完全無圖書館開放時間，生成模型正確回答無法確認。 |

### 日期、數字與引用人工核對
- 核對 [cleaned_text.txt](cleaned_text.txt) 原文：
  - `chunk 0`：競賽日期 **2026年12月15日**，時間 **上午9點至下午5點**，地點 **資訊大樓三樓創客空間**（與 [rag_record.json](rag_record.json) 引用之 `[來源2]` 完全一致）。
  - `chunk 1`：報名截止日期 **2026年12月1日**，每隊 **3至5人**，錄取 **15隊**，總名額上限 **75人**。
  - `chunk 2`：簡報 **5分鐘**，第一名獎金 **新臺幣10000元**，第二名 **6000元**（與 [integrated_rag_record-6.json](integrated_rag_record-6.json) 回答之金額一致）。

---

## 3. 課堂練習與整合 App 四類問題比較（9-1 B 紀錄表 & 10-2 檢查）

| 問題類型 | 紀錄檔案 | 預期證據 | 實際取回片段（`chunk_id` 與分數） | 回答與來源核對 | 原文支持判讀（檢索 vs 生成） |
| --- | --- | --- | --- | --- | --- |
| **原句**：`活動地點在哪裡？`（`min_score=0.2`） | [integrated_rag_record.json](integrated_rag_record.json) | `chunk 0` | `chunk 0 (0.4590)`、`chunk 2 (0.3180)` | 「活動地點為圖書館討論室。[來源1]」 | **原文支持**：`[來源1]` 對應內建範例 `chunk 0`（「地點為圖書館討論室」）。 |
| **同題改參數**：`活動地點在哪裡？`（`min_score=0.4`） | [integrated_rag_record-2.json](integrated_rag_record-2.json) | `chunk 0` | `chunk 0 (0.4590)` | 「活動地點在圖書館討論室。[來源1]」 | **原文支持**：將 `min_score` 由 `0.2` 調高至 `0.4` 後，成功在檢索階段排除無關的 `chunk 2 (0.3180)`。 |
| **改寫**：`這場讀書交流辦在哪個空間？` | [integrated_rag_record-3.json](integrated_rag_record-3.json) | `chunk 0` | `chunk 0 (0.6844)`、`chunk 2 (0.4043)` | 「這場讀書交流活動辦在圖書館討論室。[來源1]」 | **原文支持**：真實語意向量克服「地點→哪個空間」的用詞差異，生成引用正確。 |
| **資訊未提供**：`參加費用是多少？` | [integrated_rag_record-4.json](integrated_rag_record-4.json) | `chunk 2` | `chunk 2 (0.5820)`、`chunk 1 (0.4041)` | 「根據目前文件，無法確認這個問題。」 | **正確承認不足**：原文 `chunk 2` 寫「報名網址與費用尚未提供」，模型未猜測金額。 |
| **文件外**：`火星的平均氣溫是多少？` | [integrated_rag_record5.json](integrated_rag_record5.json) | 沒有 | `[]`（最高分 `0.1275` 低於門檻 `0.2`） | 「根據目前文件，無法確認這個問題。」 | **檢索階段直接攔截**：無片段達門檻 `0.2`，直接回不足句（0 次 Responses）。 |
| **自訂文件（有答案）**：`第一名獎金是多少錢？` | [integrated_rag_record-6.json](integrated_rag_record-6.json) | `chunk 2` | `chunk 2 (0.5501)`、`chunk 3 (0.2379)` | 「第一名獎金為新臺幣10000元。[來源1]」 | **原文支持**：`[來源1]` 對應黑客松文件 `chunk 2`，金額完全正確。 |
| **自訂文件（無答案）**：`學校游泳池幾點開放？` | [integrated_rag_record-7.json](integrated_rag_record-7.json) | 沒有 | `chunk 0 (0.3221)`、`chunk 1 (0.2669)` | 「根據目前文件，無法確認這個問題。」 | **生成階段正確把關**：雖有片段過門檻，但模型讀完 `context` 後正確回答無法確認。 |

---

## 4. 錯誤／邊界處理與重測紀錄
1. **邊界情境 A（`build_context` 長度上限與不修改原資料）**：
   - 在實作 `TODO A` (`build_context`) 時，需為每筆 `hit` 加上 `[來源1]`、`[來源2]` 標籤，並檢查加入該段後 `len("\n\n".join(parts + [part]))` 是否超過 `max_chars`。
   - 若超過 `max_chars` 則立即 `break` 停止（不將段落切半），並使用 `item = dict(hit)` 複製字典再寫入 `"label"`，確保不汙染原始 `hits`，通過第 4 節 `A自我檢查` 全部斷言。
2. **錯誤修正與重測紀錄 B（問題文字與跨平台換行核對）**：
   - **預期與實際**：第一次在整合版 App 測試文件外問題時，誤輸入為「`火星的平均氣溫是？`」（漏打「多少」兩字），導致 Notebook `10-2` 檢查第一項顯示 `❌ 真實API：內建範例問完四類問題`。
   - **修正與重測**：回到整合版 App 重新輸入完整問題「`火星的平均氣溫是多少？`」並下載 [integrated_rag_record5.json](integrated_rag_record5.json)，再次執行 `10-2` 檢查即拿到 4 個 `✅` 全數通過。

---

## 5. 自行建置 RAG 的限制說明（3～5 句）
1. **檢索排名不一定等於最佳證據**：如本次 [rag_record.json](rag_record.json) 詢問黑客松「活動地點在哪裡？」時，原文寫「舉辦地點」的 `chunk 0` 分數（`0.3882`）反而略低於含有「活動當日」字眼的 `chunk 3`（`0.4159`），若 `top_k` 設為 `1` 就會漏掉真正答案。
2. **切塊與門檻參數需人工反覆調校**：空白行分段或固定字元切塊可能把跨段落的上下文切斷；而 `min_score` 設太高會漏掉改寫題的證據、設太低則會把無關段落塞進 `context` 干擾生成。
3. **每次查詢重算向量無法應付大量文件**：本週教學版 App 在每次送出問題時都會把文件片段與問題重新送出向量化（或僅保存在單次 `session_state`），當文件數量變多時會造成延遲與重複計費，實務上需搭配向量資料庫或平台索引持久化保存。
4. **有標註 `[來源n]` 不代表內容零幻覺**：`check_answer` 僅能檢查格式是否包含合法來源標籤，無法保證模型沒有曲解原文或看錯數字，最終仍須人工回到原文逐項查核。

---

## 6. API 請求次數與未測項目
- **本次實際 API 請求次數**：
  - 練習版 App（3 份 `rag_record*.json`）：3 次 `embeddings.create` ＋ 3 次 `responses.create` ＝ **6 次**。
  - 整合版 App（7 份 `integrated_rag_record*.json`，含補測 1 次）：文件向量 3 次 ＋ 問題向量 7 次 ＋ 回答生成 7 次 ＝ **17 次**。
- **未測項目**：OpenAI File Search 平台代管檢索、掃描型 PDF 之 OCR 辨識、以及 Streamlit Community Cloud 雲端部署（本週皆為選讀／不列入基本作業）。

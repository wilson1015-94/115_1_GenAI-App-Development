# 第 10 週作業｜Embedding 與語意搜尋實作與驗證紀錄

## 1. 環境版本與執行模式
- **作業作者**：李承威
- **Python 與套件實際版本**：Python `3.14.0`、Streamlit `1.63.0`、OpenAI SDK `2.49.0`、python-dotenv `1.2.3`
- **執行模式與模型**：
  - 離線規則對照：人工關鍵字 4 維計數（`demo_vector`，0 次 API）
  - 真實語意檢索：真實 Embeddings API（模型：`text-embedding-3-small`）
- **啟動方式**：
  ```zsh
  cd week10/week10_semantic_search_revised
  python -m streamlit run student/app.py
  ```

---

## 2. 回家作業自訂文件與人工核對（日期與數字）
- **自訂虛構文件**：[cleaned_text.txt](cleaned_text.txt)（「校園AI創新黑客松競賽辦法」），共 4 個段落（`chunk 0`～`chunk 3`）：
  - `chunk 0`（位置 `0:60`）：競賽日期為 **2026年12月15日**，時間為 **上午9點至下午5點**，舉辦地點在 **資訊大樓三樓創客空間**。
  - `chunk 1`（位置 `62:109`）：報名截止日期為 **2026年12月1日**，每隊限 **3至5人**，錄取 **15隊**，總名額上限 **75人**。
  - `chunk 2`（位置 `111:162`）：完成 5 分鐘簡報，**第一名獎金為新臺幣10000元**，第二名 **6000元**。
  - `chunk 3`（位置 `164:207`）：免費提供午餐便當與飲水；明確記載「**交通補助與住宿安排尚未提供**」。

---

## 3. 回家作業：三類問題搜尋比較與原文判讀

| 問題類型 | 模式與模型 | 預期片段 | 實際 `chunk_id` 與分數 | 原文是否支持／證據判讀 |
| --- | --- | --- | --- | --- |
| **1. 原句題**：`第一名獎金是多少錢？`<br>（[search_record3.json](search_record3.json)） | 真實 Embeddings API (`text-embedding-3-small`) | `chunk 2` | `chunk 2`（分數 `0.5500`，位置 `111:162`） | **支持**：回原文核對 `chunk 2`，明確記載「第一名獎金為新臺幣10000元，第二名6000元」，數字完全一致。 |
| **2. 改寫題**：`這場比賽在哪個場地舉行`<br>（[search_record4.json](search_record4.json)） | 真實 Embeddings API (`text-embedding-3-small`) | `chunk 0` | 第 1 名：`chunk 0`（分數 `0.4118`，位置 `0:60`）<br>第 2 名：`chunk 2`（分數 `0.3750`，位置 `111:162`） | **支持**：原文寫「競賽／舉辦地點」，問題改寫為「比賽／哪個場地舉行」，在離線關鍵字規則下因無「地點」字眼會找不到，但真實 Embedding 向量成功將 `chunk 0`（「舉辦地點在資訊大樓三樓創客空間」）排在第 1 名。 |
| **3. 文件外題（證據不足）**：`學校游泳池幾點開放？` | 真實 Embeddings API ／ 離線規則 | 沒有 | 離線規則：`[]`；真實模式下雖有相對最高分片段，但分數偏低且無原文依據 | **證據不足**：整份黑客松競賽辦法完全未提及游泳池開放時間，回原文核對無任何支持證據，不可用來生成肯定答案。 |

*(附註：課堂預設範例「社團讀書交流活動」之實測紀錄亦一併保留於 [search_record.json](search_record.json) 與 [search_record-2.json](search_record-2.json)。)*

---

## 4. 兩組參數比較與第 9-1 節讀回驗證

1. **回家作業黑客松文件紀錄（[search_record3.json](search_record3.json) 與 [search_record4.json](search_record4.json)）**：
   - 在 `top_k = 2, min_score = 0.0`（[search_record4.json](search_record4.json)）時，除了第 1 名真正包含場地資訊的 `chunk 0`（分數 `0.4118`）外，第 2 名也會帶出同屬比賽規範但與場地無關的 `chunk 2`（分數 `0.3750`）。
   - 當調整為 `top_k = 1`（或將 `min_score` 門檻調高至 `0.40`）時，即可只保留第 1 名支持答案的核心片段，排除次要干擾段落。
2. **課堂讀書會文件同一題兩組 `top_k` 對照（[search_record.json](search_record.json) vs [search_record-2.json](search_record-2.json)）**：
   - 固定問題「`活動地點在哪裡？`」，比較 `top_k = 2`（回傳 `chunk 0: 0.4589`、`chunk 2: 0.3180`）與 `top_k = 1`（僅保留 `chunk 0: 0.4589`），驗證調整滑桿僅在本機重排，**0 次額外 API 請求**。
3. **第 9-1 節讀回驗證結果**：
   - 四份下載紀錄（`search_record.json`、`search_record-2.json`、`search_record3.json`、`search_record4.json`）均通過第 9-1 節程式檢查：
     - `scores == sorted(scores, reverse=True)`（分數由高到低排序）
     - `len(scores) <= top_k`（筆數不超過 `top_k`）
     - `hit["text"] == source[hit["start"]:hit["end"]]`（片段文字與原文起訖位置 `start:end` 完全一致）
     - `hit["score"] >= min_score`（所有片段皆不低於門檻）

---

## 5. 錯誤／邊界處理與重測紀錄
- **邊界情境**：在離線關鍵字規則下輸入改寫題「`這場比賽在哪個場地舉行`」或文件外問題「`學校游泳池幾點開放？`」時，因問題未包含預設的 4 組關鍵字，算出的 `query_vector` 為全零向量 `[0.0, 0.0, 0.0, 0.0]`。
- **預期與處理方式**：
  - `cosine_similarity` 遇到長度（norm）為 0 的向量時回傳 `0.0`，防止除以零錯誤。
  - `rank_chunks` 開頭透過 `if not any(query_vector): return []` 攔截全零問題向量，直接回傳空清單 `[]`，避免在 `min_score = 0.0` 時把所有 0 分片段誤當成搜尋結果回傳。
  - 在 `rank_chunks` 內使用 `hit = dict(item)` 複製字典後再加入 `"score"`，確保不修改原始 `chunks`，並通過第 5 節 `A自我檢查`。

---

## 6. API 請求次數與限制
- **實際 API 請求次數**：
  - 課堂預設文件實測：1 次 `embeddings.create`（下載 `search_record.json` 與 `search_record-2.json`，滑桿重排 0 次 API）。
  - 回家作業自訂黑客松文件實測：3 種問題各搜尋 1 次，共 3 次 `embeddings.create`（下載 `search_record3.json` 與 `search_record4.json`）。
- **限制說明**：
  - 相似度分數只代表向量方向接近程度，**並非答案正確機率**；即使在文件外問題取得最高分片段，仍必須回到原文核對是否有實質證據。

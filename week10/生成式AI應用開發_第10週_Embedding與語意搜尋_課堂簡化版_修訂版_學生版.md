<!-- 第1格 | w10r-cover -->

# 第10週｜Embedding與語意搜尋・修訂版（學生版）

本週流程：**已核對的片段 → 向量 → 相似度 → 找出相關片段 → 回到原文確認**。
第9週處理資料品質；本週只負責「找資料」；第11週才根據找到的證據產生回答。
<font color="#C62828"><b>重要：</b></font>相似度不是答案正確的機率；找到一段文字，也不代表它真的能回答問題。
配套App見[README](week10_semantic_search_revised/README.md)。

<!-- 第2格 | w10r-goals -->

## 0 先備、學習目標與150分鐘安排

先備：第2週list／dict、函式、sorted與lambda；第7週表單與session_state；第9週片段與來源回查。
不需要先學NumPy矩陣、ChromaDB／FAISS，也不用再寫PDF／Word讀取程式。

完成本週後，你能夠：
- 說明「意思相近的句子，向量方向也會接近」，以及為什麼文件和問題要用同一個模型。
- 讀懂cosine相似度，知道分數不是正確機率。
- 完成A：把分數變成保留來源、可回查的排名結果。
- 完成B：用原句、改寫、資訊未提供、文件外四種問題，判斷排名是否真的有原文支持。

| 時間 | 核心活動 |
|---|---|
| 15分鐘 | 第9～11週地圖、從第9週接入資料 |
| 20分鐘 | Embedding直覺與手寫小向量 |
| 20分鐘 | cosine示範與分數判讀 |
| 25分鐘 | A：來源保留、門檻與排序，自我檢查與修正 |
| 25分鐘 | 離線規則對照、真實API示範（或教師實測紀錄）、B觀察 |
| 30分鐘 | 把A移入App、改參數與來源核對 |
| 15分鐘 | 互看、錯誤與作業說明 |

合計150分鐘，另留休息10分鐘與排障20分鐘。必做A與B；只做一個App。

<!-- 第3格 | w10r-setup -->

## 1 環境、金鑰與費用

- **在哪裡執行：**Notebook看概念與短例子；Streamlit App在本機VS Code終端機啟動。本機沿用Python 3.14；Colab的Python版本由平台決定。
- **需要哪些套件：**相似度與排序只用Python內建模組；真實API與App需要openai、python-dotenv與streamlit，不需要向量資料庫。
- **金鑰放哪裡：**本機放環境變數或`week10_semantic_search_revised/.env`（Notebook與App共用）；Colab在Secrets設定OPENAI_API_KEY並授權Notebook；App部署到Streamlit Cloud時在平台的Secrets設定。金鑰不要寫進Notebook或程式。
- **會呼叫幾次API：**需要付費的格子都有自己的開關，預設關閉。Notebook的真實示範把3段文件與4個問題合成1次請求；App每次有效提交1次。
- **不能放什麼資料：**真實模式會把文件與問題送到OpenAI，不可放個資、機密或未授權資料。
- timeout=60是每次網路等待的秒數，不保證整個任務在60秒內結束。
- **程式格開頭的註解：**「先備」是要先執行的格子（包含間接需要的）；「用到前面格子定義的變數／函式」列出這格直接用到的名稱與出處，例如`rank_chunks ← 第5節A格`；若有「模組：」那一行，是前面格子匯入的套件。出現NameError時，先回去執行那一格。

<!-- 第4格 | w10r-install -->

```python
# 用途：顯示環境；先備：無；0次API。只有要用真實API或App時才需要安裝。
# Colab：取消下一行註解後執行。本機：依README用python -m pip安裝。
# %pip install openai==2.49.0 python-dotenv==1.2.3
import sys
print("Python：", sys.version)
```

<!-- 第5格 | w10r-units -->

## 2 從第9週接入：片段與來源

本週資料直接沿用第9週：`sample.txt`經過清理後的文字（也就是第9週App「下載清理後文字」的內容）。
依空白行分段，每一段當作一個片段（檢索單位），保留chunk_id與來源，之後才能回到原文核對。
下一格把這份文字分成3段，並列出本週固定使用的4個問題；Notebook與App用的是同一份資料與問題。

| 問題類型 | 問題 | 預期能支持答案的片段 |
|---|---|---|
| 原句 | 活動地點在哪裡？ | chunk 0（地點為圖書館討論室） |
| 改寫 | 這場讀書交流辦在哪個空間？ | chunk 0（用字不同，意思相同） |
| 資訊未提供 | 參加費用是多少？ | chunk 2（原文寫「費用尚未提供」） |
| 文件外 | 火星的平均氣溫是多少？ | 沒有，整份文件都沒談這件事 |

<!-- 第6格 | w10r-data -->

```python
# 用途：第9週清理後文字分段，並列出本週的4個問題；先備：無；0次API。
document = '社團讀書交流活動\n活動日期為2026年11月11日，時間是下午2點至4點，地點為圖書館討論室。\n\n報名截止日期為2026年11月6日。每組4人，共8組，總名額32人。\n\n參加者先閱讀短文，再分組討論資料來源與原文查核。報名網址與費用尚未提供。'

# 依空白行分段：每段一個片段，保留編號與來源（App用同樣的分法）
chunks = []
for paragraph in document.split("\n\n"):
    if paragraph.strip():
        chunks.append({"chunk_id": len(chunks), "source": "第9週sample.txt", "text": paragraph.strip()})

questions = [
    {"type": "原句", "query": "活動地點在哪裡？"},
    {"type": "改寫", "query": "這場讀書交流辦在哪個空間？"},
    {"type": "資訊未提供", "query": "參加費用是多少？"},
    {"type": "文件外", "query": "火星的平均氣溫是多少？"},
]
for item in chunks:
    print(item["chunk_id"], repr(item["text"]))
```

<!-- 第7格 | w10r-embedding -->

## 3 Embedding：把文字變成可以比較的數字

Embedding模型把一段文字轉成一串數字（向量）。關鍵直覺是：**意思相近的句子，向量的方向也會接近**；所以即使用字不同（「在哪裡」和「哪個空間」），也可能找到同一段。
- 文件和問題必須用**同一個模型**轉成向量，維度相同才能比較。
- Embeddings API只回傳向量；它不會建立資料庫、不會找來源，也不會產生回答。

先用手寫的2維向量建立直覺。假設維度1代表「和地點有關的程度」、維度2代表「和費用有關的程度」：

| 句子 | 手寫向量（地點, 費用） |
|---|---|
| 問題：活動在哪裡？ | (1.0, 0.1) |
| 地點為圖書館討論室 | (0.9, 0.2) |
| 報名網址與費用尚未提供 | (0.1, 0.9) |
| 每組4人，總名額32人 | (0.2, 0.3) |

這些數字是人工設定的，只為了教「方向」；真實模型的向量有上千維，每一維也沒有可以直接讀懂的意義。

<!-- 第8格 | w10r-cosine -->

## 4 Cosine相似度：比較方向，不是正確率

cosine＝兩個向量的內積 ÷ 兩個長度的乘積，範圍約在−1到1：方向相同接近1，互相垂直是0。
它不是機率：0.8不代表「答案80%正確」，也沒有適用所有資料的固定門檻。
下一格的cosine_similarity完整提供；再下一格用第3節的手寫向量算一次，看看「問地點」最接近哪一句。

<!-- 第9格 | w10r-syntax -->

### 4-1 讀程式需要的短語法

| 語法 | 在cosine_similarity或A的哪裡 | 做什麼 |
|---|---|---|
| `zip(a, b)` | `dot = sum(x * y for x, y in zip(a, b))` | 把兩個向量的數字一對一配對；先檢查長度，避免zip悄悄截短 |
| `sum(... for ...)` | 同上 | 把每一對乘積加總，不必先建立完整list |
| `all(...)`、`math.isfinite` | 檢查有限數字那一行 | 每個數字都要是有限值，排除NaN或無限大 |
| `any(vector)` | A的已提供檢查 | 至少有一個數字不是0；全零代表沒有方向 |
| `dict(item)` | A的TODO | 複製一份片段資料，再加score，避免改到原本的chunks |
| `results[:top_k]` | A的TODO | 取前k筆；不足k筆時就回傳現有的筆數 |
| `key=lambda item: item["score"]` | A的TODO | 排序時依score排；`reverse=True`由高到低（第2週學過） |

<!-- 第10格 | w10r-cosine-fn -->

```python
# 用途：完整提供的cosine相似度（App使用同一個函式）；先備：無；0次API。


def cosine_similarity(a, b):
    """完整提供：計算方向相似度；零向量回傳0，不能解讀為有語意證據。"""
    import math   # 放在函式內：Notebook與App可單獨複製這個函式使用
    if not a or len(a) != len(b):
        raise ValueError("向量不可為空且維度必須相同")
    if not all(type(x) in (int, float) and math.isfinite(x) for x in a + b):
        raise ValueError("向量必須是有限數字")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return max(-1.0, min(1.0, dot / (norm_a * norm_b)))
```

<!-- 第11格 | w10r-cosine-example -->

```python
# 用途：用第3節的手寫向量算相似度；先備：第4-1節cosine函式格；0次API。
# 用到前面格子定義的變數／函式（請先執行那些格子）：
#   cosine_similarity ← 第4-1節cosine函式格
question = [1.0, 0.1]                         # 問題：活動在哪裡？
sentences = {
    "地點為圖書館討論室": [0.9, 0.2],
    "報名網址與費用尚未提供": [0.1, 0.9],
    "每組4人，總名額32人": [0.2, 0.3],
}
for text, vector in sentences.items():
    print(f"{cosine_similarity(question, vector):.3f}", text)

# 邊界：全零向量沒有方向，回傳0，不代表語意已被理解
print("全零向量：", cosine_similarity([0.0, 0.0], [1.0, 0.0]))
```

<!-- 第12格 | w10r-cosine-result -->

預期「地點為圖書館討論室」最高（約0.99），「費用」那句最低。方向接近就是分數高，這正是語意搜尋的基本原理。
但「每組4人」也有約0.6的分數：分數高低是相對的，不能看到正數就當成有關，還是要回原文判斷。

<!-- 第13格 | w10r-ranking -->

## 5 A：把分數變成可回查的排名（必做，約20分鐘含修正）

| 項目 | 說明 |
|---|---|
| 已提供 | 參數檢查（top_k、min_score、筆數）、向量可計算的檢查、問題向量全零時回傳[] |
| 你負責 | ① 逐筆算score；② score ≥ min_score才保留；③ 用dict(item)複製並加score；④ 由高到低排序；⑤ 取前top_k筆 |
| 輸入 | chunks（list[dict]）、同順序的vectors、query_vector、top_k、min_score |
| 回傳 | list[dict]，每筆保留原來源欄位並多一個score；沒有合格片段就回傳[] |
| 結果保存 | 下一格自我檢查把結果存到hits_result |
| 執行順序 | 第4節cosine函式格 → A格 → A自我檢查格；App使用同一個函式 |

要用return回傳，只print的話後面拿不到；不可直接在原本的dict加score。排序語法見4-1。

<!-- 第14格 | w10r-a -->

```python
# 用途：練習A排名函式（App使用同一個函式）；先備：第4-1節cosine函式格；0次API。
# 用到前面格子定義的變數／函式（請先執行那些格子）：
#   cosine_similarity ← 第4-1節cosine函式格


def rank_chunks(chunks, vectors, query_vector, top_k=3, min_score=0.0):
    """傳入片段與同順序向量，回傳附score的來源資料；不呼叫API。"""
    # 已提供：參數與資料檢查。
    if type(top_k) is not int or top_k <= 0:
        raise ValueError("top_k須為正整數")
    if not isinstance(min_score, (int, float)) or not -1 <= min_score <= 1:
        raise ValueError("min_score須介於-1與1")
    if len(chunks) != len(vectors):
        raise ValueError("片段與向量筆數不一致")
    if not chunks:
        return []
    # 已提供：先確認向量都能計算；問題向量全零就回傳空結果，不硬塞一筆。
    for vector in vectors:
        cosine_similarity(vector, query_vector)
    if not any(query_vector):
        return []

    # TODO A：
    # 1. 逐筆用cosine_similarity算出score；score >= min_score才保留。
    # 2. 用dict(item)複製來源資料，再加入"score"欄位（不可改到原本的chunks）。
    # 3. 依score由高到低排序，回傳前top_k筆；沒有合格片段就回傳[]。
    raise NotImplementedError("請完成TODO A：來源保留、篩選與排序")
```

<!-- 第15格 | w10r-a-check -->

```python
# 用途：A自我檢查（固定資料，不需修改）；先備：第4-1節cosine函式格、第5節A格；0次API。
# 用到前面格子定義的變數／函式（請先執行那些格子）：
#   rank_chunks ← 第5節A格
hits_result = None
try:
    check_chunks = [
        {"chunk_id": 10, "source": "測試.txt", "text": "第一段"},
        {"chunk_id": 11, "source": "測試.txt", "text": "第二段"},
        {"chunk_id": 12, "source": "測試.txt", "text": "第三段"},
    ]
    check_vectors = [[0.0, 1.0], [1.0, 0.0], [0.8, 0.6]]
    hits_result = rank_chunks(check_chunks, check_vectors, [1.0, 0.0], 2, 0.5)
    assert [item["chunk_id"] for item in hits_result] == [11, 12]   # 由高到低、門檻與top_k
    assert all(item["source"] == "測試.txt" for item in hits_result)  # 來源保留
    assert "score" not in check_chunks[0]                             # 原資料沒被改
    assert rank_chunks(check_chunks, check_vectors, [1.0, 0.0], 5, 0.99) == hits_result[:1]  # 門檻很高只剩1筆
    assert rank_chunks(check_chunks, check_vectors, [0.0, 0.0]) == []  # 全零問題
    print("A通過：排序、門檻、top_k、來源保留與不修改原資料")
except NotImplementedError as exc:
    print(exc)
```

<!-- 第16格 | w10r-a-result -->

A應顯示通過訊息。常見錯誤：
- 順序反了：檢查reverse。
- 原資料被改：是不是直接在原本的dict加了score。
- 筆數不對：檢查篩選與切片的順序（先篩選、再排序、最後取前k筆）。

請保留一次「失敗→修正→重測」，或另外設計一筆空結果的邊界資料。通過自我檢查只證明程式功能正確，不代表語意搜尋品質好。

<!-- 第17格 | w10r-offline -->

## 6 離線對照：人工關鍵字規則

沒有金鑰時，可以先用demo_vector跑通流程：它把文字中出現的關鍵字分4組計數，**不是模型學出來的語意向量**。
下一格用第2節的4個問題跑一次，請特別注意「改寫」那題：原文寫「地點」，問題寫「哪個空間」，規則沒收這些字，就會找不到。
離線規則與真實向量不能混用，分數也不能互相比較。

<!-- 第18格 | w10r-demo-fn -->

```python
# 用途：完整提供的離線規則向量（App使用同一個函式）；先備：無；0次API。


def demo_vector(text):
    """完整提供：人工指定4組關鍵字計數，不是模型學到的語意向量。"""
    groups = [
        ["地點", "圖書館", "討論室", "哪裡"],   # 第1維：地點
        ["報名", "截止"],                       # 第2維：報名
        ["名額", "每組", "人數", "幾人"],       # 第3維：人數
        ["費用", "多少錢", "網址"],             # 第4維：費用與網址
    ]
    vector = []
    for words in groups:
        vector.append(float(sum(text.count(word) for word in words)))
    return vector
```

<!-- 第19格 | w10r-offline-run -->

```python
# 用途：用離線規則跑4個問題；先備：第2節資料格、第4-1節cosine函式格、第5節A格、第6節離線規則函式格；0次API。
# 用到前面格子定義的變數／函式（請先執行那些格子）：
#   chunks、questions ← 第2節資料格
#   rank_chunks ← 第5節A格
#   demo_vector ← 第6節離線規則函式格
offline_results = None
try:
    vectors = [demo_vector(item["text"]) for item in chunks]
    offline_results = []
    for q in questions:
        hits = rank_chunks(chunks, vectors, demo_vector(q["query"]), top_k=2, min_score=0.1)
        offline_results.append({"type": q["type"], "query": q["query"], "hits": hits})
        found = [(hit["chunk_id"], round(hit["score"], 3)) for hit in hits]
        print(q["type"], q["query"], "→", found or "找不到")
except NotImplementedError as exc:
    offline_results = None   # 未完成A時不保留一半的結果
    print(exc)
```

<!-- 第20格 | w10r-offline-result -->

預期：原句與費用題找得到；**改寫題找不到**（問題裡沒有規則收錄的關鍵字，向量全是0）；文件外題也找不到。
這說明關鍵字比對的限制：用字不同就失效。下一節用真實Embedding，看看同一個改寫問題能不能找到chunk 0。

<!-- 第21格 | w10r-real -->

## 7 真實Embeddings API：同一批文件與問題

下一格把第2節的3段文件與4個問題，用同一個模型一次轉成向量。RUN_REAL_EMBEDDINGS預設False（0次）；改成True後執行一次是1次請求，不會產生回答。
1. 7段文字（3段文件＋4個問題）一次送出。
2. 回傳的每筆有index，依index排回原本的順序。
3. 前3個是文件向量，後4個是問題向量；檢查筆數、維度、數值都合格才保存embedding_result，失敗會清掉舊資料。

資料很小，所以合成一批送出；實務上會保存文件向量，之後只需要向量化新問題。官方說明：[Embeddings](https://developers.openai.com/api/docs/guides/embeddings)。

<!-- 第22格 | w10r-real-run -->

```python
# 用途：同一模型一次向量化3段文件與4個問題；先備：第2節資料格；預設0次API，開啟後1次。
# 用到前面格子定義的變數／函式（請先執行那些格子）：
#   chunks、questions ← 第2節資料格
import math
import os
import sys

RUN_REAL_EMBEDDINGS = False   # 改成True才會真的呼叫API
embedding_result = None
embedding_error = None
documents = [item["text"] for item in chunks]
query_texts = [q["query"] for q in questions]

if RUN_REAL_EMBEDDINGS:
    try:
        from dotenv import load_dotenv
        from openai import OpenAI

        # 1. 讀金鑰：本機用環境變數或App資料夾的.env（與App共用）；在Colab則讀Secrets
        load_dotenv("week10_semantic_search_revised/.env")   # 先讀App資料夾的.env
        load_dotenv()                                         # 再找目前資料夾往上的.env
        key = os.getenv("OPENAI_API_KEY", "")
        if "google.colab" in sys.modules:
            from google.colab import userdata
            key = userdata.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("請先設定並授權OPENAI_API_KEY")

        # 2. 文件＋問題合成一批，用同一個模型送出（1次請求）
        model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        inputs = documents + query_texts
        with OpenAI(api_key=key, max_retries=0, timeout=60.0) as client:
            response = client.embeddings.create(model=model, input=inputs, encoding_format="float")

        # 3. 依index排回原順序，再檢查筆數、維度與數值
        ordered = sorted(response.data, key=lambda item: item.index)
        if [item.index for item in ordered] != list(range(len(inputs))):
            raise ValueError("回傳向量筆數或順序不合格")
        vectors = [item.embedding for item in ordered]
        for vector in vectors:
            if not vector or len(vector) != len(vectors[0]):
                raise ValueError("向量為空或維度不一致")
            if not all(type(x) in (int, float) and math.isfinite(x) for x in vector) or not any(vector):
                raise ValueError("向量含非有限數字或全零")
        embedding_result = {"model": model, "documents": documents,
                            "questions": query_texts, "vectors": vectors}
        print("已保存真實向量：", len(vectors), "筆，每筆", len(vectors[0]), "維")
    except Exception as exc:
        embedding_error = f"本次未保存向量：{type(exc).__name__}：{exc}"
        print(embedding_error)
else:
    print("RUN_REAL_EMBEDDINGS=False：已略過API，尚未取得真實語意向量")
```

<!-- 第23格 | w10r-real-result -->

### 7-1 用真實向量排名4個問題

下一格用剛才保存的向量排名，不會再呼叫API；沒有執行真實API時只會提示「未測」，不會用離線規則冒充。
先寫下你預期每題會找到哪一段，再看結果；特別比較「改寫」題和第6節離線規則的差別。
文件外的問題仍然會有一個最高分的片段，要回到原文判斷它是不是真的能回答。

老師課前實跑時，可把SAVE_TEACHER_RECORD改成True，存下排名紀錄（不含向量）供沒有API的同學觀察。

<!-- 第24格 | w10r-real-rank -->

```python
# 用途：用已保存的真實向量排名；先備：第2節資料格、第4-1節cosine函式格、第5節A格、第7節真實API格；0次新API。
# 用到前面格子定義的變數／函式（請先執行那些格子）：
#   rank_chunks ← 第5節A格
#   embedding_result ← 第7節真實API格
import json
from datetime import datetime, timezone
from pathlib import Path

SAVE_TEACHER_RECORD = False   # 老師課前實測時改成True，存成teacher_ranking_record.json
real_rankings = None
if embedding_result is None:
    print("尚未取得真實向量：B的真實語意觀察寫「未測」，或看7-2的教師實測紀錄")
else:
    try:
        count = len(embedding_result["documents"])
        real_chunks = [{"chunk_id": i, "source": "第9週sample.txt", "text": text}
                       for i, text in enumerate(embedding_result["documents"])]
        real_rankings = []
        for offset, query in enumerate(embedding_result["questions"]):
            hits = rank_chunks(real_chunks, embedding_result["vectors"][:count],
                               embedding_result["vectors"][count + offset], 2, 0.0)
            real_rankings.append({"query": query, "hits": hits})
            print(query, "→", [(hit["chunk_id"], round(hit["score"], 3)) for hit in hits])
        if SAVE_TEACHER_RECORD:
            record = {"note": "教師課前實測紀錄，不是本次執行結果",
                      "recorded_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                      "model": embedding_result["model"], "rankings": real_rankings}
            Path("teacher_ranking_record.json").write_text(
                json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
            print("已存teacher_ranking_record.json（不含向量）")
    except NotImplementedError as exc:
        print(exc)
```

<!-- 第25格 | w10r-teacher-record -->

### 7-2 沒有API時：看老師課前的實測紀錄

如果老師有提供teacher_ranking_record.json，把它放在Notebook所在的資料夾，執行下一格就能看到真實Embedding的排名。
這是**老師的實測紀錄**，請在B表的「模式」欄寫「教師實測紀錄（日期、模型）」，不要寫成自己執行的結果。
沒有這個檔案時，B的真實語意欄寫「未測」即可。

<!-- 第26格 | w10r-teacher-record-run -->

```python
# 用途：讀老師課前存下的真實排名紀錄；先備：teacher_ranking_record.json在目前資料夾；0次API。
import json
from pathlib import Path

teacher_record = None
path = Path("teacher_ranking_record.json")
if path.exists():
    teacher_record = json.loads(path.read_text(encoding="utf-8"))
    print(teacher_record["note"], "｜", teacher_record["recorded_at_utc"], "｜", teacher_record["model"])
    for item in teacher_record["rankings"]:
        print(item["query"], "→", [(hit["chunk_id"], round(hit["score"], 3)) for hit in item["hits"]])
else:
    print("沒有教師實測紀錄：B的真實語意欄寫「未測」")
```

<!-- 第27格 | w10r-b -->

## 8 B：同一份資料，四種問題與兩組參數（必做觀察）

TODO B：沿用同一份資料，不另寫第二個搜尋器。把結果填入8-1的表格：
1. 四種問題各記一列：預期片段、實際排名與分數、原文是否支持。沒有證據就寫「不足」。
2. 固定一個問題，只改一個參數（top_k=1與2，或兩個不同門檻），記下哪些片段增加或消失。
3. 記一次錯誤或邊界與處理，例如問題空白、規則全零、門檻太高全部排除、API失敗；不能補造模型結果。

Notebook的排名重用已保存的向量、App的滑桿在本機重排，都不會再呼叫API；只有送出新文字或新問題才會多算一次。
沒有API時，可用離線規則加上7-2的教師實測紀錄完成；兩者都要標明模式。

<!-- 第28格 | w10r-b-reference -->

### 8-1 B紀錄表

| 問題類型 | 模式（離線／自己的API／教師實測） | 預期片段 | 實際chunk_id與分數 | 原文是否支持／限制 |
|---|---|---|---|---|
| 原句：活動地點在哪裡？ | 待填 | chunk 0 | 待填 | 待填 |
| 改寫：這場讀書交流辦在哪個空間？ | 待填 | chunk 0 | 待填 | 待填 |
| 資訊未提供：參加費用是多少？ | 待填 | chunk 2 | 待填 | 待填 |
| 文件外：火星的平均氣溫是多少？ | 待填 | 沒有 | 待填 | 待填 |
| 參數比較（同一題，k或門檻二選一） | 待填 | — | 待填 | 待填 |

分數高卻沒有原文支持，要記為「檢索不足」，不能拿來生成肯定的答案。
「資訊未提供」和「文件外」要分清楚：前者原文明確寫了「尚未提供」，後者整份文件根本沒談這件事。

<!-- 第29格 | w10r-app -->

## 9 把A移入同一個Streamlit App

student/app.py只有A待完成：把通過自我檢查的rank_chunks貼到同名函式。cosine、離線規則與畫面都已提供。
- App的預設文字就是第2節的第9週清理後文字；也可以貼上自己第9週App下載的cleaned_text.txt。以空白行分段，最多12段。
- 每個片段保留start／end，可回到貼入的文字核對位置。App不會匯入第9週的JSON。
- 預設離線模式0次API；勾選真實模式後，每次有效提交1次請求（文件與問題合成一批）。改top_k或門檻滑桿只在本機重排，不會再呼叫API。
- 表單改了但沒提交，畫面仍是上次成功結果；切換模式、清除或新提交失敗都會清掉舊結果。A未完成時不會送出付費請求。
- 下載的搜尋紀錄包含模式、模型、原文、問題與排名，不含金鑰與整批向量。這是小文件教學App，不是正式的大型索引。

<!-- 第30格 | w10r-download-check -->

### 9-1 下載後重新讀回與回查

在App按「下載搜尋紀錄」，把search_record.json放到Notebook所在的資料夾（Colab：拖進左側「檔案」窗格），再執行下一格。沒有檔案時只會提示，不用示意檔假裝驗證過。
下一格檢查：每個片段的text等於source[start:end]、分數由高到低且不低於門檻、筆數不超過top_k。通過只代表紀錄能回到原文，片段是否真的支持答案，仍要自己讀原文判斷。
作業要下載兩份紀錄；第二份檔名可能變成search_record (1).json，改下一格的path再執行一次。

<!-- 第31格 | w10r-download-run -->

```python
# 用途：驗證自己從App下載的搜尋紀錄；先備：search_record.json在Notebook所在的資料夾；0次API。
import json
from pathlib import Path

search_record = None
path = Path("search_record.json")
if path.exists():
    search_record = json.loads(path.read_text(encoding="utf-8"))
    print(search_record["mode"], "｜", search_record["model"], "｜問題：", search_record["query"])
    scores = [hit["score"] for hit in search_record["hits"]]
    assert scores == sorted(scores, reverse=True), "分數沒有由高到低"
    assert len(scores) <= search_record["top_k"], "筆數超過top_k"
    for hit in search_record["hits"]:
        assert hit["text"] == search_record["source"][hit["start"]:hit["end"]], "片段和原文位置對不上"
        assert hit["score"] >= search_record["min_score"], "有片段低於門檻"
        print("chunk", hit["chunk_id"], "｜分數", round(hit["score"], 3), "｜", hit["text"][:40])
    print("實際下載檔回查通過，片段數：", len(search_record["hits"]))
else:
    print("尚未找到下載檔：完成App下載後再執行本格")
```

<!-- 第32格 | w10r-homework -->

## 10 回家作業：同一個App的搜尋證據（45～60分鐘）

沿用A與同一個App，換一份合法、無敏感資料的小文件（可用自己第9週作業的清理後文字），或自己寫3～6段虛構內容。題目自選，最低要求固定。
1. 用原句、改寫、文件外三種問題各搜尋一次；至少一題找到支持來源，一題判斷證據不足。
2. 固定同一題，比較兩組top_k或門檻，說明理由，並下載兩份搜尋紀錄JSON，各用9-1讀回一次。
3. 記錄一個錯誤或邊界的預期、實際、修正與重測；人工核對一個日期或數字。

繳交：學生Notebook（A自我檢查＋B紀錄表）、同一個App、文件或貼入文字、兩份搜尋紀錄JSON、README。截圖或文字證據擇一即可。
請求次數：老師示範1次；你在App問三種問題各1次，共3次。改滑桿與下載不會再呼叫API，額外重跑請另外記次數。
沒有API時，先記離線功能與限制，真實語意欄寫「未測」；可引用教師實測紀錄，但要標明來源。

| 評量 | 證據 |
|---|---|
| A功能與來源（40%） | 自我檢查、自己的邊界資料、原資料不被改寫 |
| B比較與判讀（30%） | 三類問題、兩組參數、支持片段或不足理由；區分離線、自己API與教師紀錄 |
| 錯誤修正（20%） | 一個錯誤或邊界、處理與重測 |
| 可重現與反思（10%） | README含實際版本、模式、來源、限制與請求次數 |

推送到整學期使用的Repo；老師從既有Google表單登記的Repo查看，不另交連結。ChromaDB／FAISS、RAG回答、File Search與部署都不列入本週基本作業。

<!-- 第33格 | w10r-bridge -->

## 11 下一週：把檢索接到RAG與File Search

| 路線 | 第11週怎麼做 | 本週準備了什麼 |
|---|---|---|
| 自行建置 | 用本週的片段＋向量＋排名找證據 → 組成context → 模型回答並附來源 | rank_chunks與「回原文核對」的習慣 |
| OpenAI File Search | 上傳支援格式的文件，由平台負責切塊、向量化、索引與檢索 | 知道平台做了哪些事，以及仍要自己核對原文 |

本週用普通list看懂資料流；向量資料庫（如ChromaDB）的價值是管理大量向量與來源，細節留給自主選讀。
兩條路線都要核對資料、證據與資訊不足的情況；第11週擇一實作即可。本週只有檢索，沒有產生回答，也沒有呼叫file_search。
官方說明：[Embeddings](https://developers.openai.com/api/docs/guides/embeddings)｜[Retrieval](https://developers.openai.com/api/docs/guides/retrieval)｜[File Search](https://developers.openai.com/api/docs/guides/tools-file-search)

<!-- 第34格 | w10r-checklist -->

## 12 完成檢核

- [ ] 能說明「意思相近→向量方向接近」，以及文件和問題要用同一個模型。
- [ ] 能分清片段、向量、相似度、檢索與回答。
- [ ] A只負責排名：來源保留、門檻與top_k正確，不在函式裡呼叫API。
- [ ] 知道分數不是機率，也沒有通用門檻；離線規則找不到改寫題是規則限制。
- [ ] 四種問題都有原文判讀，沒有證據不補造；教師紀錄有標明來源。
- [ ] App改滑桿不新增API，失敗不留舊結果；README記了模式、版本與請求次數。
- [ ] 下載的搜尋紀錄已放回Notebook，用9-1讀回並通過。

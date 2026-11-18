# 第10週片段搜尋・修訂版（學生版）
# 用途：文字→向量→A排名→回到原文確認；不產生回答。
# 啟動：在week10/week10_semantic_search_revised執行
# python -m streamlit run student/app.py
# 預設離線規則0次API；真實模式每次有效提交最多1次，滑桿重排0次。
# 學生只補A；輸入、API與狀態完整提供，不另寫第二套App。

import json
import math
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 金鑰：Cloud讀平台Secrets；本機讀.env或環境變數（見read_setting）。
# 先讀week10_semantic_search_revised/.env（Notebook也讀同一份），再讀入口資料夾的.env；已有的值不會被覆蓋。
load_dotenv(Path(__file__).resolve().parents[1] / '.env')
load_dotenv(Path(__file__).resolve().parent / '.env')
st.set_page_config(page_title='文件片段搜尋', layout='centered')


# ---------- 1. 完整提供的短函式與A練習 ----------
def read_setting(name, default=""):
    """完整提供：平台Secrets優先，本機使用環境變數或本資料夾的.env。"""
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except FileNotFoundError:
        return os.getenv(name, default)


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


# ---------- 2. 模式與成功資料 ----------
st.title("文件片段搜尋")
st.caption("先找支持問題的原文，不生成答案。請勿輸入個資、機密或未授權內容。")
real_api = st.checkbox("使用真實Embeddings API（可能產生費用）", value=False)
st.caption("預設是離線關鍵字規則，不是語意模型；換句話說的問題可能找不到。真實模式每次有效提交最多1次API。")
st.session_state.setdefault("record", None)
st.session_state.setdefault("error", "")
# 切換模式時，舊結果來自另一種向量，直接清除
if st.session_state.get("real_api_mode") != real_api:
    st.session_state.record = None
    st.session_state.error = ""
    st.session_state.real_api_mode = real_api
if st.button("清除結果"):
    st.session_state.record = None
    st.session_state.error = ""

# ---------- 3. 表單：貼入第9週確認過的文字與問題 ----------
# 預設文字＝第9週sample.txt清理後的結果；也可貼上第9週App下載的cleaned_text.txt內容。
sample = (Path(__file__).resolve().parents[1] / "sample_data/week09_cleaned_text.txt").read_text(encoding="utf-8")
with st.form("search_form"):
    source = st.text_area("文件文字（空白行分段；可貼第9週的清理後文字）", value=sample, height=210)
    query = st.text_input("查詢問題（範例見sample_data/questions.json）", value="活動地點在哪裡？")
    submitted = st.form_submit_button("建立向量並搜尋")

if submitted:
    st.session_state.record = None  # 新提交失敗時，不能沿用舊的成功資料。
    st.session_state.error = ""
    try:
        # ---------- 4. 輸入檢查與分段：全在本機 ----------
        source = source.replace("\r\n", "\n").replace("\r", "\n")
        if not source.strip() or len(source) > 6000:
            raise ValueError("文件須有1到6000字元，不會默默截斷")
        if not query.strip() or len(query) > 300:
            raise ValueError("問題須有1到300字元")
        chunks = []
        cursor = 0
        for paragraph in source.split("\n\n"):
            text = paragraph.strip()
            if text:
                if len(text) > 1000:
                    raise ValueError("每段最多1000字元，請先確認並分段")
                start = source.find(text, cursor)   # 記下這段在貼入文字中的位置
                end = start + len(text)
                chunks.append({
                    "chunk_id": len(chunks), "source": "貼入文字",
                    "start": start, "end": end, "text": text,
                })
                cursor = end
        if len(chunks) > 12:
            raise ValueError("最多12段，請縮小教學文件範圍")
        # 付費前先試跑A：A未完成會在這裡停止，0次API。
        rank_chunks([{"chunk_id": 0, "source": "檢查", "text": "檢查"}], [[1.0]], [1.0])
        inputs = [item["text"] for item in chunks] + [query]

        # ---------- 5. 文件與問題用同一種向量 ----------
        if real_api:
            key = read_setting("OPENAI_API_KEY")
            if not key:
                raise ValueError("缺少OPENAI_API_KEY，請設定.env或平台Secrets")
            model = read_setting("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            # 小型教學批次：文件＋問題合併成1次請求；每次新提交都重新向量化。
            # 正式服務應保存文件向量，之後只向量化新問題；本例不做跨次快取。
            with OpenAI(api_key=key, max_retries=0, timeout=60.0) as client:
                response = client.embeddings.create(
                    model=model, input=inputs, encoding_format="float",
                )
            # 依index排回送出的順序，再檢查筆數、維度與數值
            ordered = sorted(response.data, key=lambda item: item.index)
            if [item.index for item in ordered] != list(range(len(inputs))):
                raise ValueError("向量回傳筆數或順序不合格")
            vectors = [item.embedding for item in ordered]
            for vector in vectors:
                if not vector or len(vector) != len(vectors[0]) or not any(vector):
                    raise ValueError("向量為空、全零或維度不一致")
                if not all(type(x) in (int, float) and math.isfinite(x) for x in vector):
                    raise ValueError("向量含非有限數字")
            mode = "真實Embeddings API"
        else:
            vectors = [demo_vector(text) for text in inputs]
            model = "人工關鍵字4維；非語意模型"
            mode = "離線規則示範"
        # 兩種向量不可混用；保存本次原文、模型與同批向量，供滑桿在本機重排。
        st.session_state.record = {
            "mode": mode, "model": model, "source": source,
            "query": query, "chunks": chunks, "vectors": vectors,
        }
    except NotImplementedError as exc:
        st.session_state.error = str(exc)
    except ValueError as exc:
        st.session_state.error = str(exc)
    except Exception as exc:
        st.session_state.error = "本次未保存結果，請檢查模型、網路或額度。錯誤類型：" + type(exc).__name__

# ---------- 6. 只在本機重排：改滑桿不會再呼叫API ----------
top_k = st.slider("最多顯示幾段（top_k）", 1, 5, 2)
min_score = st.slider("最低分數（不是正確機率）", 0.0, 1.0, 0.0, 0.05)
if st.session_state.error:
    st.error(st.session_state.error)
if st.session_state.record is not None:
    record = st.session_state.record
    try:
        hits = rank_chunks(
            record["chunks"], record["vectors"][:-1],
            record["vectors"][-1], top_k, min_score,
        )
        st.caption("以下為上次成功提交的結果；表單改了但沒提交，原文與問題不會更新。")
        st.write("模式：", record["mode"], "模型：", record["model"])
        st.write("本次問題：", record["query"])
        if not hits:
            st.warning("沒有可用片段；請檢查關鍵字規則、門檻與原文，不能補造答案。")
        for item in hits:
            st.write(f"chunk {item['chunk_id']}｜分數 {item['score']:.4f}｜來源 {item['source']}｜位置 {item['start']}:{item['end']}")
            st.write(item["text"])
        with st.expander("核對本次原文"):
            st.text(record["source"])
        # 只匯出原文與排名結果；不寫入金鑰或整批高維向量。
        export = {
            "mode": record["mode"], "model": record["model"],
            "query": record["query"], "source": record["source"],
            "top_k": top_k, "min_score": min_score, "hits": hits,
        }
        st.download_button(
            "下載搜尋紀錄", json.dumps(export, ensure_ascii=False, indent=2),
            "search_record.json", mime="application/json",
        )
    except (ValueError, NotImplementedError) as exc:
        st.error(str(exc))

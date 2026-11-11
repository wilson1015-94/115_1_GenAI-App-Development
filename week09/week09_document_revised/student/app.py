# ============================================================
# 第9週文件前處理・修訂版（學生版）
# 教學重點：讀取→清理→切塊→檢查→成功保存→預覽與下載。
# 啟動：在week09/week09_document_revised內執行
# python -m streamlit run student/app.py
# 本App全程離線，0次API；AI選做另見Notebook，不需金鑰。
# 學生只完成A清理；讀取、切塊與畫面已完整提供。
# ============================================================

import csv
import json
import re
from io import BytesIO, StringIO
from pathlib import Path

import streamlit as st


# ---------- 1. A清理練習與完整切塊函式 ----------
def clean_text(text: str) -> str:
    """TODO A：傳入str，回傳保留段落、合併行內空白的新字串。"""
    # 已提供：統一換行，之後只需處理\n。
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    # TODO A：
    # 1. 逐行合併多餘空白（參考第4節的示範）。
    # 2. 連續空白行最多保留一個（參考4-1的re.sub）。
    # 3. 去掉頭尾空白後return；日期、數字、標點不能刪。
    raise NotImplementedError("請完成TODO A：文字清理")


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[dict]:
    """以字元滑動視窗切塊；位置指向清理後文字，end不包含在片段內。"""
    # 完整提供：學生在活動B使用與觀察，不需改寫迴圈。
    if chunk_size <= 0:
        raise ValueError("chunk_size必須大於0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap須滿足0 <= overlap < chunk_size")
    if not text.strip():
        return []

    # 1. 從起點往前切，保留切片原樣，讓來源位置可以精確核對。
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        content = text[start:end]
        if content.strip():
            chunks.append({
                "chunk_id": len(chunks),
                "start": start,
                "end": end,
                "text": content,
            })

        # 2. 已到結尾就停止；否則下一段從end往回overlap個字元開始。
        if end == len(text):
            break
        start = end - overlap
    return chunks


# ---------- 2. 完整提供：多格式讀取 ----------
def extract_text(filename: str, data: bytes, encoding: str = "utf-8-sig") -> str:
    """依副檔名讀取，統一回傳str；完整提供，不是學生TODO。"""
    suffix = Path(filename).suffix.lower()

    # 1. TXT／MD（同2-1）與CSV（同3-1）：先解碼；不用errors="ignore"悄悄丟掉內容。
    if suffix in (".txt", ".md"):
        return data.decode(encoding)
    if suffix == ".csv":
        reader = csv.DictReader(StringIO(data.decode(encoding)))
        if not reader.fieldnames or any(not name.strip() for name in reader.fieldnames):
            raise ValueError("CSV需要非空欄名")
        if len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError("CSV欄名不可重複")
        lines = []
        for number, row in enumerate(reader, start=1):
            if number > 200:
                raise ValueError("CSV限200列資料；請先縮小範圍")
            if None in row or None in row.values():
                raise ValueError("CSV列與欄名數量不一致")
            fields = []
            for name, value in row.items():
                fields.append(f"{name}={value}")
            lines.append(f"第{number}列：" + "；".join(fields))
        return "\n".join(lines)

    # 2. PDF（同3-2）：只有讀PDF才需要pypdf；缺套件不影響TXT先跑通。
    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(data))
        if reader.is_encrypted:
            raise ValueError("請改用未加密PDF")
        if len(reader.pages) > 50:
            raise ValueError("PDF限50頁；請先縮小範圍")
        pages = []
        has_text = False
        for number, page in enumerate(reader.pages, start=1):
            content = (page.extract_text() or "").strip()
            if content:
                has_text = True
            pages.append(f"[第{number}頁]\n" + (content or "[此頁無文字層，請回看原檔]"))
        if not has_text:
            raise ValueError("PDF無可抽取文字，可能需要OCR；空白頁也可能沒有文字")
        return "\n\n".join(pages)

    # 3. DOCX（同3-3）：依本文順序讀段落與表格，避免先列段落再補表格而改變順序。
    if suffix == ".docx":
        from docx import Document
        from docx.text.paragraph import Paragraph
        parts = []
        for item in Document(BytesIO(data)).iter_inner_content():
            if isinstance(item, Paragraph):
                parts.append(item.text)
            else:
                for row in item.rows:
                    values = [cell.text for cell in row.cells]
                    if any(value.strip() for value in values):
                        parts.append(" | ".join(values))
        return "\n\n".join(parts)

    raise ValueError("僅支援TXT、MD、CSV、PDF、DOCX")


# ---------- 3. 輸入與參數 ----------
SAMPLE_FOLDER = Path(__file__).resolve().parents[1] / "sample_data"   # 與Notebook相同的四個範例檔
st.title("文件抽取、清理與切塊")
st.caption("全程本機處理，0次API；按「處理文件」才讀取。請使用無敏感資料的小文件。")

# 表單把資料來源與參數一起送出，避免每調一次就重新解析PDF或Word。
with st.form("document_form"):
    source = st.radio("資料來源", ["內建範例", "上傳檔案"], horizontal=True)
    sample_name = st.selectbox("內建範例（與Notebook相同）", ["sample.txt", "sample.csv", "sample.pdf", "sample.docx"])
    uploaded = st.file_uploader(
        "上傳文件（資料來源選「上傳檔案」時使用）",
        type=["txt", "md", "csv", "pdf", "docx"],
        max_upload_size=1,
    )  # 未選檔為None；type只篩副檔名，內容仍須檢查。
    encoding = st.selectbox("TXT／CSV編碼（上傳檔案時使用）", ["utf-8-sig", "cp950"])
    size = st.slider("chunk_size（字元）", 40, 1000, 120, 20)
    overlap = st.number_input("overlap（字元）", min_value=0, value=20, step=10)
    submitted = st.form_submit_button("處理文件")

# ---------- 4. 處理與成功保存 ----------
# session_state保存上次提交成功的結果；表單改值但沒送出，不會更新結果。
if "document_result" not in st.session_state:
    st.session_state.document_result = None
if st.button("清除結果"):
    st.session_state.document_result = None

if submitted:
    # 新提交先清舊結果：這次失敗時，不會留下前次成功的下載。
    st.session_state.document_result = None
    try:
        # 4-1. 取得bytes：內建範例用read_bytes，上傳檔案用getvalue
        if source == "內建範例":
            filename = sample_name
            data = (SAMPLE_FOLDER / filename).read_bytes()
            encoding = "utf-8-sig"   # 範例檔都是UTF-8
        elif uploaded is not None:
            filename = uploaded.name
            data = uploaded.getvalue()
        else:
            raise ValueError("請上傳檔案，或改選內建範例")
        if len(data) > 1024 * 1024:
            raise ValueError("檔案限1MB")

        # 4-2. 與Notebook第6節相同順序：抽取→清理→檢查長度→切塊
        raw_text = extract_text(filename, data, encoding)
        cleaned_text = clean_text(raw_text)
        if not cleaned_text or len(cleaned_text) > 20000:
            raise ValueError("清理後須有1到20000字元；請檢查原文或縮小範圍")
        chunks = chunk_text(cleaned_text, size, int(overlap))
        if not chunks:
            raise ValueError("沒有可用片段")

        # 4-3. 全部成功才保存；位置以cleaned_text為準，不是PDF座標。
        st.session_state.document_result = {
            "filename": filename,
            "encoding": encoding,
            "character_count": len(cleaned_text),
            "chunk_size": size,
            "overlap": int(overlap),
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "chunks": chunks,
        }
    except NotImplementedError as exc:
        st.warning(str(exc))  # TODO未完成就提示，不把骨架當作處理成功。
    except (ValueError, UnicodeError) as exc:
        st.error(f"輸入或參數不合格：{exc}")
    except ImportError:
        st.error("缺少PDF／Word讀取套件；請在目前環境安裝本資料夾的requirements.txt")
    except Exception as exc:
        st.error(f"讀取失敗（{type(exc).__name__}），請檢查格式、檔案是否損壞或另存後再試")

# ---------- 5. 顯示與匯出：只用已保存的結果，不重新讀檔 ----------
record = st.session_state.document_result
if record is not None:
    st.caption("以下為上次成功提交的結果；改了檔案或參數，請再按「處理文件」。")
    st.write({key: record[key] for key in ["filename", "character_count", "chunk_size", "overlap"]})
    st.text_area("抽取原文", record["raw_text"], disabled=True, height=160)
    st.text_area("清理後文字", record["cleaned_text"], disabled=True, height=160)
    st.write(f"片段數：{len(record['chunks'])}")
    # 選片段只重新顯示，不重新讀取檔案。
    selected = st.selectbox("預覽chunk_id", range(len(record["chunks"])))
    st.json(record["chunks"][selected])
    st.download_button(
        "下載chunks JSON",
        data=json.dumps(record, ensure_ascii=False, indent=2),
        file_name="document.chunks.json",
        mime="application/json",
    )  # JSON含清理後文字，下載後可核對start:end是否對得上。
    st.download_button(
        "下載清理後文字（第10週貼入用）",
        data=record["cleaned_text"],
        file_name="cleaned_text.txt",
        mime="text/plain",
    )  # 第10週App以空白行分段，直接貼這份文字即可。

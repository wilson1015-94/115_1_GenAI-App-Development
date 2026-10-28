# ============================================================
# 04 非串流聊天與前文保存
# ------------------------------------------------------------
# 教學重點：
#   1. 先重畫已完成紀錄，再處理這次問題。
#   2. 送出最近五輪與本次問題，模型才取得指定前文。
#   3. 成功才保存完整問答；切換模式或按清空就清除本機紀錄。
#
# 啟動：python -m streamlit run student/04_chat.py
# 請先進入week07/week07_streamlit_simple配套資料夾，並使用課程環境。
# 預設離線，0次請求；啟用API後每次有效問題最多1次。
# ============================================================

import os

# 將Streamlit簡稱為st；下方st.xxx用來建立網頁元件或存取狀態。
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.title("課程聊天助理")  # st.title顯示頁面的主標題。


# ---------- 1. API開關與聊天狀態 ----------
# 預設只做離線畫面示範；勾選後還要送出問題才會請求。
# st.checkbox建立勾選框並回傳True／False；value=False讓它預設不勾選，勾選本身不會呼叫API。
enable_api = st.checkbox("啟用真實API（每則問題1次請求）", value=False)
# st.caption用較小字體顯示補充說明，適合放操作提示與限制。
st.caption(
    "預設離線固定回覆，只測畫面與保存；"
    "不代表模型理解或記住前文。切換模式會清空紀錄。"
)

# messages保存完成的user／assistant配對；chat_mode記錄它們來自哪個模式。
# st.session_state是目前工作階段的保存空間；下方先檢查鍵是否存在，避免每次重跑都重設。
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_mode = enable_api

# 切換離線／真實模式時清空，避免把固定假回答當成模型前文送出。
if st.session_state.chat_mode != enable_api:
    st.session_state.messages = []
    st.session_state.chat_mode = enable_api


# ---------- 2. 清空或重畫已完成的對話 ----------
# 清空只修改本機history，不會發出API請求，也不會取消先前費用。
# st.button建立按鈕；只有點擊當次回傳True，其餘重新執行為False，供下方if判斷。
if st.button("清空聊天紀錄"):
    st.session_state.messages = []

# 每次rerun都重畫保存的紀錄；畫面上看到歷史，不代表API自動取得它。
for message in st.session_state.messages:
    # st.chat_message依角色建立聊天訊息容器；with區塊內的元件會放進這則訊息，不會自動保存前文。
    with st.chat_message(message["role"]):
        # st.write將這筆歷史訊息的文字放進目前的聊天容器。
        st.write(message["content"])


# ---------- 3. 取得這次問題，準備要送出的前文 ----------
# 沒有提交時prompt為None；空白問題也不進入下方處理。
# st.chat_input建立聊天輸入框；送出時回傳本次文字，未送出時為None，這裡最多1000字元。
prompt = st.chat_input("請輸入問題（最多1000字元）", max_chars=1000)
if prompt and prompt.strip():
    # 先顯示本次問題，但尚未加入正式紀錄；本輪失敗就不保存半輪。
    # st.chat_message依角色建立聊天訊息容器；with區塊內的元件會放進這則訊息，不會自動保存前文。
    with st.chat_message("user"):
        # st.write把本次問題放進user容器；正式紀錄仍在成功後保存。
        st.write(prompt)

    # 畫面紀錄不是模型記憶；必須將最近五輪與本輪問題放進API的input。
    # [-10:]選最近10則完成訊息；這裡只裁切送出的內容，不裁切本機保存。
    messages = st.session_state.messages[-10:] + [{"role": "user", "content": prompt}]

    try:

        # ---------- 4. 取得完整回答，再顯示 ----------
        if enable_api:

            # --- 4-1. 檢查金鑰，建立不自動重試的client ---
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                raise ValueError("缺少金鑰")
            client = OpenAI(api_key=key, max_retries=0, timeout=60.0)

            # --- 4-2. 送出一次非串流請求 ---
            # input明確帶上前文；本例不使用previous_response_id接續對話。
            # instructions每輪重送。store=False不代表原文不離開本機。
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
                store=False,
                instructions="你是課程助理，回答簡潔；不確定就說明，不憑空補充。",
                input=messages,
            )

            # --- 4-3. 拒答、未完成或空回答，不進入成功保存區 ---
            # 先查拒答：請求收到回應，不代表模型提供了可採用的答案。
            # output可能包含不同類型的項目；只在message的content中找拒答標記。
            for output in response.output:
                if output.type == "message":
                    for content in output.content:
                        if content.type == "refusal":
                            raise ValueError("模型拒答")

            # 再確認狀態完成且文字非空；通過後才交給下方解析或保存。
            # 這裡只查完成與文字，內容是否忠於原文仍需人工覆核。
            if response.status != "completed" or not response.output_text.strip():
                raise ValueError("沒有完成的非空回答")


            answer = response.output_text

        else:
            # 固定文字只測介面與保存流程；不能用來證明模型記得前文。
            answer = "離線畫面示範：已收到「" + prompt + "」，沒有呼叫模型。"

        # st.chat_message依角色建立聊天訊息容器；with區塊內的元件會放進這則訊息，不會自動保存前文。
        with st.chat_message("assistant"):
            # st.write把完整回答放進assistant容器。
            st.write(answer)

    except Exception as exc:
        # 可能已顯示使用者問題或部分回答，但不會因此寫入正式history。
        # st.error顯示錯誤提示；不會自行丟出例外或停止程式，也不代表結果已保存。
        st.error("這輪未加入紀錄；請檢查設定或回應。錯誤類型：" + type(exc).__name__)

    else:
        # ---------- 5. 本輪完整成功，才保存下一輪會用到的前文 ----------
        # 只有完整成功才保存user與assistant配對；失敗不留半輪。
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": answer})

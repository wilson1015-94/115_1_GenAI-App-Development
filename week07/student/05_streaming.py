# ============================================================
# 05 串流顯示與完成後保存
# ------------------------------------------------------------
# 教學重點：
#   1. 沿用04的資料流，改以yield和st.write_stream逐段顯示。
#   2. 文字片段不等於完成；拒答、失敗或缺完成事件都不保存。
#   3. 串流函式已完整提供，課堂先理解顯示與保存的責任。
#
# 啟動：python -m streamlit run student/05_streaming.py
# 請先進入week07/week07_streamlit_simple配套資料夾，並使用課程環境。
# 預設離線，0次請求；啟用API後每次有效問題最多1次。
# ============================================================

import os

# 將Streamlit簡稱為st；下方st.xxx用來建立網頁元件或存取狀態。
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ---------- 0. 完整提供的串流函式：教師帶讀，不要求學生重寫 ----------
# 呼叫generator函式先取得可迭代物件；st.write_stream取用時才逐步執行。
def stream_answer(messages):
    """完整提供的串流段：逐片yield，確認完成後才結束。"""

    # --- 0-1. 檢查設定，準備本次請求 ---
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("缺少金鑰")
    client = OpenAI(api_key=key, max_retries=0, timeout=60.0)

    # 出現文字片段還不算成功；必須收到completed且狀態完成。
    completed = False

    # --- 0-2. 接收事件，分開處理文字、完成與失敗 ---
    # with確保失敗或中止離開時關閉串流連線。
    # 關閉本機連線不保證遠端取消或免計費；本例不在這裡自行重試。
    with client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        store=False,
        instructions="你是課程助理，回答簡潔；不確定就說明，不憑空補充。",
        input=messages,
        stream=True,
    ) as events:
        for event in events:
            if event.type == "response.output_text.delta":
                # yield交出一段文字給顯示端，再等顯示端取下一段。
                yield event.delta

            elif event.type == "response.completed":
                completed = event.response.status == "completed"

                # 完成事件仍檢查是否含拒答；拒答不當作正常聊天答案。
                for output in event.response.output:
                    if output.type == "message":
                        for content in output.content:
                            if content.type == "refusal":
                                raise ValueError("模型拒答")

            elif event.type in [
                "error",
                "response.failed",
                "response.incomplete",
                "response.refusal.delta",
                "response.refusal.done",
            ]:
                # 已顯示的片段也可能失敗；拋出錯誤，阻止外層保存。
                raise ValueError("串流失敗、未完成或拒答")

    # --- 0-3. 串流結束仍須確認真的收到完成事件 ---
    if not completed:
        raise ValueError("沒有收到完成事件")

st.title("課程聊天助理：串流版")  # st.title顯示頁面的主標題。


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

        # ---------- 4. 逐段顯示回答，檢查完整字串 ----------
        # st.chat_message依角色建立聊天訊息容器；with區塊內的元件會放進這則訊息，不會自動保存前文。
        with st.chat_message("assistant"):
            if enable_api:
                # 若generator中途拋錯，就直接交給except，不會進入成功保存。
                # st.write_stream逐段取用並顯示文字；本例全是文字，所以正常結束後回傳串接完成的字串。
                answer = st.write_stream(stream_answer(messages))

            else:
                # 固定片段只示範串接，不是模型成果，也不測量回應速度。
                # st.write_stream逐段取用並顯示文字；本例全是文字，所以正常結束後回傳串接完成的字串。
                answer = st.write_stream(["離線片段示範：", "已收到「", prompt, "」，沒有呼叫模型。"])

        # 函式正常完成後，再確認得到非空文字；畫面片段不等於正式紀錄。
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("沒有完整的非空回答")

    except Exception as exc:
        # 可能已顯示使用者問題或部分回答，但不會因此寫入正式history。
        # st.error顯示錯誤提示；不會自行丟出例外或停止程式，也不代表結果已保存。
        st.error("這輪未加入紀錄；請檢查設定或回應。錯誤類型：" + type(exc).__name__)

    else:
        # ---------- 5. 本輪完整成功，才保存下一輪會用到的前文 ----------
        # 只有完整成功才保存user與assistant配對；失敗不留半輪。
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": answer})

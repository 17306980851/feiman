import streamlit as st
from openai import OpenAI

# --- 页面配置 ---
st.set_page_config(page_title="费曼对抗陪练", page_icon="🎓")
st.title("🎓 费曼对抗式陪练")

# --- 初始化大模型客户端 ---
try:
    API_KEY = st.secrets["mimo_token"]
except KeyError:
    st.error("未找到 Token！请在 Streamlit 的 Secrets 中配置。")
    st.stop()

# 直接套用你发的官方鉴权格式
client = OpenAI(
    api_key=API_KEY,    
    base_url="https://api.xiaomimimo.com/v1"
)

# 核心 Prompt
SYSTEM_PROMPT = """
你现在是一个极其严谨、逻辑缜密但自称“基础为零”的学生。
任务：让用户教你考研数学一的知识点。
规则：
1. 绝对禁止直接给出正确答案或公式定理。
2. 必须不断寻找用户解释中的逻辑漏洞，并给出具体的数学反例。
3. 逼迫用户用第一性原理解释专业术语。
4. 数学公式必须使用 LaTeX 格式输出。
"""

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 渲染历史对话
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- 聊天输入 ---
if prompt := st.chat_input("用大白话给我讲讲..."):
    # 记录用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 请求 API
    with st.chat_message("assistant"):
        try:
            # 使用官方文档中的模型名称
            response = client.chat.completions.create(
                model="mimo-v2.5-pro", 
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1024
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"接口调用出错了: {e}")

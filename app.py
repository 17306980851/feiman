import streamlit as st
import requests

# --- 页面配置 ---
st.set_page_config(page_title="费曼对抗陪练", page_icon="🎓")
st.title("🎓 费曼对抗式陪练")

# --- 读取 Token (防泄漏机制) ---
try:
    API_KEY = st.secrets["mimo_token"]
except KeyError:
    st.error("未找到 Token！请在 Streamlit 的 Secrets 中配置。")
    st.stop()

# ⚠️ 注意：这里需要替换为你从小平台官方文档里查到的真实 API 接口地址！
API_URL = "https://api.xiaomimimo.com/v1/chat/completions"
SYSTEM_PROMPT = """
你现在是一个极其严谨、逻辑缜密但自称“基础为零”的学生。
任务：让用户教你考研数学一的知识点。
规则：
1. 绝对禁止直接给出正确答案或公式定理。
2. 必须不断寻找用户解释中的逻辑漏洞，并给出具体的数学反例。
3. 逼迫用户用第一性原理解释专业术语。
4. 数学公式必须使用 LaTeX 格式。
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("用大白话给我讲讲..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "MiMo-V2.5", # 确保模型名称与小米文档一致
            "messages": st.session_state.messages,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status() 
            answer = response.json()['choices'][0]['message']['content']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"接口调用出错了，检查一下URL或者网络: {e}")

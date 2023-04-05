
# 以下を「app.py」に書き込み
import openai
import streamlit as st

import secret_keys

openai.api_key = secret_keys.openai_api_key

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
    ]

def communicate(input_text, messages):
    user_message = {"role": "user", "content": input_text}
    messages.append(user_message)

    if len(messages) % 2 == 0:
        bot_id = 1
    else:
        bot_id = 2

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=messages[-1]["content"],
        max_tokens=1024,
        temperature=0.7,
        n=1,
        stop=None,
        user=messages[-1]["role"] + str(bot_id)
    )

    bot_message = response.choices[0].text.strip()
    messages.append({"role": f"bot{bot_id}", "content": bot_message})

    return messages

st.title("My AI Assistant")
st.write("OpenAI APIを使ったチャットボットです。")

if "messages" in st.session_state:
    messages = st.session_state["messages"]
else:
    messages = []
st.write("以下は過去のメッセージです。")
for message in messages:
    st.write(f"{message['role']}: {message['content']}")

user_input = st.text_input("メッセージを入力してください。", key="user_input")
if st.button("送信"):
    messages = communicate(user_input, messages)
    st.session_state["messages"] = messages

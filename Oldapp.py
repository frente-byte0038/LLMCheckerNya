import streamlit as st
import ollama
from PIL import Image
import io

# --- ページ設定 ---
st.set_page_config(page_title="Simple Checker LLM", layout="wide")

st.title("🤖 Simple Checker LLM")
st.caption("Ollamaのモデルを比較して「床の強度」を点検するコクピット")

# --- サイドバー：モデルの管理と人格設定 ---
with st.sidebar:
    st.header("設定")
    model_names = []
    try:
        models_info = ollama.list()
        if hasattr(models_info, 'models'):
            model_names = [m.model for m in models_info.models]
        elif isinstance(models_info, dict) and 'models' in models_info:
            model_names = [m.get('model', m.get('name', 'Unknown')) for m in models_info['models']]

        if not model_names:
            st.warning("モデルが見つかりません。")
    except Exception as e:
        st.error(f"接続エラー: {e}")

    compare_mode = st.checkbox("比較モード (2モデル同時出力)", value=False)
    st.divider()

    model_1 = st.selectbox("モデル 1 (メイン/Vision対応推奨)", model_names if model_names else ["なし"])
    if compare_mode:
        model_2 = st.selectbox("モデル 2 (比較用)", model_names if model_names else ["なし"])

    st.divider()
    system_prompt = st.text_area(
        "システムプロンプト (人格設定)",
        value="あなたは熟練のFXトレーダー兼エンジニアです。チャートの事実に基づき、リスク・リワードを重視した分析を行ってください。",
        help="ここに書いた指示が、すべてのモデルの『思考の基盤』になります。"
    )

# --- 画像アップローダーの設置 ---
st.subheader("📊 チャート分析")
uploaded_file = st.file_uploader("TradingViewのスクショをアップロード", type=['png', 'jpg', 'jpeg'])
img_bytes = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="分析対象のチャート", width=600)
    img_byte_arr = io.BytesIO()
    # ✅ Fix③: format が None の場合のフォールバック
    image.save(img_byte_arr, format=image.format or "PNG")
    img_bytes = img_byte_arr.getvalue()

# --- チャット履歴の初期化（モデルごとに独立） ---
# 通常モード用
if "messages" not in st.session_state:
    st.session_state.messages = []
# 比較モード用（それぞれ独立した履歴）
if "messages_1" not in st.session_state:
    st.session_state.messages_1 = []
if "messages_2" not in st.session_state:
    st.session_state.messages_2 = []

# --- 過去のメッセージ表示 ---
if compare_mode:
    # 比較モード：model_1 の履歴をベースに表示
    for message in st.session_state.messages_1:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message:
                for img in message["images"]:
                    st.image(img, width=300)
else:
    # 通常モード
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message:
                for img in message["images"]:
                    st.image(img, width=300)

# --- ユーザー入力とAI実行 ---
if prompt := st.chat_input("FXの戦略やAIのロジックをテストしよう"):

    # ✅ Fix⑤: モデル未接続時のガード
    if not model_names:
        st.error("Ollamaに接続できていません。モデルを確認してください。")
        st.stop()

    # ユーザーメッセージの構築
    user_message = {"role": "user", "content": prompt}
    if img_bytes:
        user_message["images"] = [img_bytes]

    with st.chat_message("user"):
        st.markdown(prompt)
        if img_bytes:
            st.image(img_bytes, width=300)

    # --- 比較モード ---
    if compare_mode:
        # ✅ Fix②: それぞれの履歴にユーザーメッセージを追加
        st.session_state.messages_1.append(user_message)
        st.session_state.messages_2.append(user_message)

        base_1 = [{"role": "system", "content": system_prompt}] + st.session_state.messages_1
        base_2 = [{"role": "system", "content": system_prompt}] + st.session_state.messages_2

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"Model: {model_1}")
            with st.spinner(f"{model_1} が思考中..."):
                resp1 = ollama.chat(model=model_1, messages=base_1)
                answer1 = resp1.message.content
                st.markdown(answer1)

        with col2:
            st.success(f"Model: {model_2}")
            with st.spinner(f"{model_2} が思考中..."):
                resp2 = ollama.chat(model=model_2, messages=base_2)
                answer2 = resp2.message.content
                st.markdown(answer2)

        # ✅ Fix②: それぞれの履歴にアシスタント回答を保存
        st.session_state.messages_1.append({"role": "assistant", "content": answer1})
        st.session_state.messages_2.append({"role": "assistant", "content": answer2})

    # --- 通常モード ---
    else:
        st.session_state.messages.append(user_message)
        base_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

        with st.chat_message("assistant"):
            with st.spinner(f"{model_1} が思考中..."):
                response = ollama.chat(model=model_1, messages=base_messages)
                answer = response.message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
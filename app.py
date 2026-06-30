import streamlit as st
import ollama
from PIL import Image
import io
import subprocess
import time

# --- ページ設定 ---
st.set_page_config(page_title="LLMCheckerNya", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --sc-bg: linear-gradient(135deg, #f5efe4 0%, #e3edf7 100%);
        --sc-panel: rgba(255, 255, 255, 0.88);
        --sc-line: rgba(40, 58, 84, 0.14);
        --sc-text: #203047;
        --sc-subtle: #5b6b80;
        --sc-accent: #d86f45;
        --sc-accent-soft: rgba(216, 111, 69, 0.12);
        --sc-sidebar-bg: rgba(248, 244, 238, 0.96);
        --sc-header-bg: rgba(247, 242, 234, 0.96);
        --sc-input-bg: rgba(255, 255, 255, 0.92);
        --sc-upload-bg: rgba(255, 255, 255, 0.92);
        --sc-button-bg: #355b99;
        --sc-button-text: #ffffff;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --sc-bg: linear-gradient(135deg, #0f1724 0%, #162232 100%);
            --sc-panel: rgba(24, 34, 49, 0.90);
            --sc-line: rgba(196, 210, 228, 0.16);
            --sc-text: #edf3fb;
            --sc-subtle: #b8c6d9;
            --sc-accent: #ffb48b;
            --sc-accent-soft: rgba(255, 180, 139, 0.18);
            --sc-sidebar-bg: rgba(18, 27, 39, 0.96);
            --sc-header-bg: rgba(16, 24, 35, 0.96);
            --sc-input-bg: rgba(19, 30, 43, 0.96);
            --sc-upload-bg: rgba(22, 33, 48, 0.96);
            --sc-button-bg: #8db1ff;
            --sc-button-text: #0f1724;
        }
    }
    html[data-theme="dark"], body[data-theme="dark"], .stApp[data-theme="dark"],
    html[data-baseweb="dark"], body[data-baseweb="dark"],
    .dark, [data-testid="stApp"][data-theme-base="dark"] {
        --sc-bg: linear-gradient(135deg, #0f1724 0%, #162232 100%);
        --sc-panel: rgba(24, 34, 49, 0.90);
        --sc-line: rgba(196, 210, 228, 0.16);
        --sc-text: #edf3fb;
        --sc-subtle: #b8c6d9;
        --sc-accent: #ffb48b;
        --sc-accent-soft: rgba(255, 180, 139, 0.18);
        --sc-sidebar-bg: rgba(18, 27, 39, 0.96);
        --sc-header-bg: rgba(16, 24, 35, 0.96);
        --sc-input-bg: rgba(19, 30, 43, 0.96);
        --sc-upload-bg: rgba(22, 33, 48, 0.96);
        --sc-button-bg: #8db1ff;
        --sc-button-text: #0f1724;
    }
    html[data-theme="light"], body[data-theme="light"], .stApp[data-theme="light"],
    .light, [data-testid="stApp"][data-theme-base="light"] {
        --sc-bg: linear-gradient(135deg, #f5efe4 0%, #e3edf7 100%);
        --sc-panel: rgba(255, 255, 255, 0.88);
        --sc-line: rgba(40, 58, 84, 0.14);
        --sc-text: #203047;
        --sc-subtle: #5b6b80;
        --sc-accent: #d86f45;
        --sc-accent-soft: rgba(216, 111, 69, 0.12);
        --sc-sidebar-bg: rgba(248, 244, 238, 0.96);
        --sc-header-bg: rgba(247, 242, 234, 0.96);
        --sc-input-bg: rgba(255, 255, 255, 0.92);
        --sc-upload-bg: rgba(255, 255, 255, 0.92);
        --sc-button-bg: #355b99;
        --sc-button-text: #ffffff;
    }
    .stApp {
        background: var(--sc-bg);
        color: var(--sc-text);
    }
    .stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div, .stApp h1, .stApp h2, .stApp h3 {
        color: var(--sc-text);
    }
    [data-testid="stSidebar"] {
        background: var(--sc-sidebar-bg);
        border-right: 1px solid var(--sc-line);
    }
    [data-testid="stHeader"] {
        background: var(--sc-header-bg) !important;
        border-bottom: 1px solid var(--sc-line);
    }
    [data-testid="stHeader"] *,
    [data-testid="stToolbar"] *,
    [data-testid="stDecoration"] * {
        color: var(--sc-text) !important;
        fill: var(--sc-text) !important;
        stroke: var(--sc-text) !important;
    }
    .stMarkdown, .stCaption, .stText, .stChatMessage {
        color: var(--sc-text);
    }
    [data-testid="stSidebar"] * {
        color: var(--sc-text) !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="textarea"] > div {
        background: var(--sc-input-bg) !important;
        border-color: var(--sc-line) !important;
    }
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploaderDropzone"] * ,
    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] p,
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stChatMessageContent"] {
        color: var(--sc-text) !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: var(--sc-upload-bg) !important;
        border: 1px dashed rgba(32, 48, 71, 0.22) !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] small {
        color: var(--sc-text) !important;
    }
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploaderDropzone"] button * {
        background: var(--sc-button-bg) !important;
        color: var(--sc-button-text) !important;
        border-color: var(--sc-button-bg) !important;
        fill: var(--sc-button-text) !important;
    }
    textarea, input, select,
    .stSelectbox label, .stCheckbox label, .stTextArea label,
    [data-baseweb="select"] *,
    [data-baseweb="textarea"] *,
    [data-baseweb="input"] * {
        color: var(--sc-text) !important;
    }
    textarea, input,
    [data-baseweb="select"] > div,
    [data-baseweb="textarea"] > div,
    [data-baseweb="input"] > div {
        background: var(--sc-input-bg) !important;
        border-color: var(--sc-line) !important;
    }
    ::placeholder {
        color: var(--sc-subtle) !important;
    }
    .hero-card, .section-card, .result-card {
        background: var(--sc-panel);
        border: 1px solid var(--sc-line);
        border-radius: 22px;
        box-shadow: 0 18px 50px rgba(36, 52, 71, 0.08);
    }
    .hero-card {
        padding: 1.4rem 1.5rem 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .hero-badge {
        display: inline-block;
        padding: 0.28rem 0.65rem;
        border-radius: 999px;
        background: var(--sc-accent-soft);
        color: var(--sc-accent);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .hero-title {
        color: var(--sc-text);
        font-size: 2.2rem;
        line-height: 1.1;
        margin: 0.7rem 0 0.35rem 0;
        font-weight: 800;
    }
    .hero-copy, .section-copy {
        color: var(--sc-subtle);
        font-size: 0.98rem;
        margin: 0;
    }
    .section-title {
        color: var(--sc-text);
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 0.25rem 0;
    }
    .result-card {
        padding: 1rem 1rem 0.75rem 1rem;
        min-height: 100%;
    }
    .result-topline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 0.8rem;
    }
    .model-chip {
        display: inline-block;
        padding: 0.22rem 0.55rem;
        border-radius: 999px;
        background: rgba(53, 91, 153, 0.10);
        color: #355b99;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .result-meta {
        color: var(--sc-subtle);
        font-size: 0.82rem;
        font-weight: 600;
    }
    .summary-box {
        padding: 0.9rem 1rem;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.74);
        border: 1px solid var(--sc-line);
    }
    .summary-label {
        color: var(--sc-subtle);
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.2rem;
    }
    .summary-value {
        color: var(--sc-text);
        font-size: 1rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
      <span class="hero-badge">Local LLM Comparison</span>
      <div class="hero-title">LLMCheckerNya</div>
      <p class="hero-copy">同じ入力を複数モデルへ投げて、回答の内容や速度の違いを見比べるためのローカル比較ツールです。</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def get_running_model_names():
    try:
        running = ollama.ps()
    except Exception:
        return []

    models = getattr(running, "models", None)
    if not models:
        return []

    names = []
    for model in models:
        name = getattr(model, "model", None) or getattr(model, "name", None)
        if name:
            names.append(name)
    return names


def unload_model(model_name):
    result = subprocess.run(
        ["ollama", "stop", model_name],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return True, (result.stdout or f"{model_name} stopped").strip()
    return False, (result.stderr or result.stdout or f"failed to stop {model_name}").strip()

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
    # 比較モードOFF時も model_2 を None で初期化しておく
    model_2 = None
    if compare_mode:
        model_2 = st.selectbox("モデル 2 (比較用)", model_names if model_names else ["なし"])

    st.divider()
    system_prompt = st.text_area(
        "システムプロンプト (人格設定)",
        value="日本語で簡潔に回答してください。",
        help="ここに書いた指示が、すべてのモデルの『思考の基盤』になります。"
    )

    st.divider()
    st.subheader("モデル管理")
    running_model_names = get_running_model_names()
    if running_model_names:
        st.caption("現在ロード中のモデルをアンロードできます。次回の読み込み時間を測りたいときに使ってください。")
        for running_model_name in running_model_names:
            if st.button(f"Unload: {running_model_name}", key=f"unload_{running_model_name}", use_container_width=True):
                ok, message = unload_model(running_model_name)
                if ok:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    else:
        st.caption("現在ロード中のモデルはありません。")

# --- 入力エリア ---
st.markdown(
    """
    <div class="section-card" style="padding: 1rem 1.1rem; margin-bottom: 1rem;">
      <div class="section-title">比較入力</div>
      <p class="section-copy">テキストだけでも使えます。画像やスクリーンショットは必要なときだけ追加してください。</p>
    </div>
    """,
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader("任意: 比較したい画像やスクリーンショットをアップロード", type=['png', 'jpg', 'jpeg'])
img_bytes = None

if uploaded_file:
    image = Image.open(uploaded_file)
    preview_col, info_col = st.columns([1.25, 1], gap="large")
    with preview_col:
        st.image(image, caption="比較対象の入力画像", use_container_width=True)
    with info_col:
        with st.container(border=True):
            st.markdown("**画像入力の概要**")
            st.caption("テキスト質問と一緒に各モデルへ送信されます。")
            st.markdown(f"- ファイル名: `{uploaded_file.name}`")
            st.markdown(f"- MIME: `{uploaded_file.type or 'unknown'}`")
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format or "PNG")
    img_bytes = img_byte_arr.getvalue()

with st.form("prompt_form", clear_on_submit=True):
    prompt = st.text_area(
        "質問内容",
        height=140,
        placeholder="ここに質問や比較したい指示を書いてください。Shift+Enter で改行できます。",
    )
    st.caption("送信はボタンで行います。Shift+Enter で改行できます。")
    submitted = st.form_submit_button("送信", use_container_width=True)

if not submitted:
    prompt = None
elif prompt is not None:
    prompt = prompt.strip()

# --- チャット履歴の初期化（モデルごとに独立） ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "messages_1" not in st.session_state:
    st.session_state.messages_1 = []
if "messages_2" not in st.session_state:
    st.session_state.messages_2 = []

# --- ストリーミング用ジェネレータ ---
def stream_ollama(model, messages, metrics):
    stream = ollama.chat(model=model, messages=messages, stream=True)
    for chunk in stream:
        if getattr(chunk, "done", False):
            metrics["eval_count"] = getattr(chunk, "eval_count", None)
            metrics["eval_duration"] = getattr(chunk, "eval_duration", None)
        yield chunk.message.content


def format_generation_metrics(elapsed_seconds, metrics):
    parts = [f"応答時間: {elapsed_seconds:.1f}秒"]
    eval_count = metrics.get("eval_count")
    eval_duration = metrics.get("eval_duration")

    if eval_count and eval_duration and eval_duration > 0:
        tokens_per_second = eval_count / (eval_duration / 1_000_000_000)
        parts.append(f"{tokens_per_second:.1f} tok/s")

    return " / ".join(parts)


def render_model_result_header(model_name, elapsed_label):
    st.markdown(
        f"""
        <div class="result-topline">
          <span class="model-chip">{model_name}</span>
          <span class="result-meta">{elapsed_label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_history(history_messages, history_title):
    with st.expander(history_title, expanded=False):
        if not history_messages:
            st.caption("まだ履歴はありません。")
            return
        for message in history_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# --- ユーザー入力とAI実行 ---
if prompt:

    if not model_names:
        st.error("Ollamaに接続できていません。モデルを確認してください。")
        st.stop()

    # テキストのみの履歴保存用メッセージ（画像はバイナリなのでセッションに積まない）
    user_message_history = {"role": "user", "content": prompt}
    # モデルへ送る今回限りのメッセージ（画像を含む）
    user_message_with_image = {"role": "user", "content": prompt}
    if img_bytes:
        user_message_with_image["images"] = [img_bytes]

    st.markdown(
        """
        <div class="section-card" style="padding: 1rem 1.1rem; margin: 1rem 0 0.8rem 0;">
          <div class="section-title">今回の入力</div>
          <p class="section-copy">この条件で各モデルへ同じ内容を送信しています。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    summary_cols = st.columns(3, gap="small")
    with summary_cols[0]:
        st.markdown(
            f"""
            <div class="summary-box">
              <div class="summary-label">モデル数</div>
              <div class="summary-value">{2 if compare_mode else 1}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with summary_cols[1]:
        st.markdown(
            f"""
            <div class="summary-box">
              <div class="summary-label">画像入力</div>
              <div class="summary-value">{'あり' if img_bytes else 'なし'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with summary_cols[2]:
        target_models = f"{model_1} / {model_2}" if compare_mode else model_1
        st.markdown(
            f"""
            <div class="summary-box">
              <div class="summary-label">対象モデル</div>
              <div class="summary-value">{target_models}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.container(border=True):
        st.markdown("**入力プロンプト**")
        st.write(prompt)
        if img_bytes:
            st.image(img_bytes, width=320)

    st.markdown(
        """
        <div class="section-card" style="padding: 1rem 1.1rem; margin: 1rem 0 0.8rem 0;">
          <div class="section-title">比較結果</div>
          <p class="section-copy">モデル名と応答時間を見ながら、内容の違いを読み比べてください。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 比較モード ---
    if compare_mode:
        st.session_state.messages_1.append(user_message_history)
        st.session_state.messages_2.append(user_message_history)

        # 最新メッセージだけ画像付きで上書き
        base_1 = [{"role": "system", "content": system_prompt}] + st.session_state.messages_1[:-1] + [user_message_with_image]
        base_2 = [{"role": "system", "content": system_prompt}] + st.session_state.messages_2[:-1] + [user_message_with_image]

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                started_at = time.perf_counter()
                render_model_result_header(model_1, "応答中...")
                metrics1 = {}
                with st.chat_message("assistant"):
                    answer1 = st.write_stream(stream_ollama(model_1, base_1, metrics1))
                elapsed1 = time.perf_counter() - started_at
                render_model_result_header(model_1, format_generation_metrics(elapsed1, metrics1))

        with col2:
            with st.container(border=True):
                started_at = time.perf_counter()
                render_model_result_header(model_2, "応答中...")
                metrics2 = {}
                with st.chat_message("assistant"):
                    answer2 = st.write_stream(stream_ollama(model_2, base_2, metrics2))
                elapsed2 = time.perf_counter() - started_at
                render_model_result_header(model_2, format_generation_metrics(elapsed2, metrics2))

        st.session_state.messages_1.append({"role": "assistant", "content": answer1})
        st.session_state.messages_2.append({"role": "assistant", "content": answer2})

    # --- 通常モード ---
    else:
        st.session_state.messages.append(user_message_history)
        base_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages[:-1] + [user_message_with_image]

        with st.container(border=True):
            started_at = time.perf_counter()
            render_model_result_header(model_1, "応答中...")
            metrics = {}
            with st.chat_message("assistant"):
                answer = st.write_stream(stream_ollama(model_1, base_messages, metrics))
            elapsed = time.perf_counter() - started_at
            render_model_result_header(model_1, format_generation_metrics(elapsed, metrics))
        st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown(
    """
    <div class="section-card" style="padding: 1rem 1.1rem; margin: 1rem 0 0.6rem 0;">
      <div class="section-title">会話履歴</div>
      <p class="section-copy">比較結果を見直したいときだけ開いてください。</p>
    </div>
    """,
    unsafe_allow_html=True,
)
if compare_mode:
    history_col1, history_col2 = st.columns(2)
    with history_col1:
        render_history(st.session_state.messages_1, f"{model_1} の履歴")
    with history_col2:
        render_history(st.session_state.messages_2, f"{model_2} の履歴")
else:
    render_history(st.session_state.messages, f"{model_1} の履歴")

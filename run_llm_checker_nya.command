#!/bin/bash

# 1. Ollamaが起動していなければ起動する
if ! pgrep -x "Ollama" > /dev/null; then
    open -a Ollama
    sleep 3
fi

# 2. 外部SSDのマウント確認
if [ ! -d "/Volumes/LLMNya/projects/Simple-Checker-LLM" ]; then
    echo "Error: 外部SSD (LLMNya) がマウントされていません。"
    exit 1
fi

# 3. プロジェクトへ移動
cd "/Volumes/LLMNya/projects/Simple-Checker-LLM"

# 4. 仮想環境を有効化 ✅
source /Volumes/LLMNya/projects/Simple-Checker-LLM/.venv/bin/activate

# 5. Streamlit起動
streamlit run app.py --server.headless true &

# 6. 起動待ち（最大30秒）
echo "Waiting for Streamlit to start..."
for i in {1..15}; do
    if curl -s http://localhost:8501 > /dev/null; then
        echo "Streamlit is up! Opening browser..."
        open http://localhost:8501
        break
    fi
    echo "Still waiting... ($i/15)"
    sleep 2
    if [ $i -eq 15 ]; then
        echo "Error: Streamlit が起動しませんでした。"
        exit 1
    fi
done

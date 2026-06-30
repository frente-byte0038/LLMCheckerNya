# LLMCheckerNya

`LLMCheckerNya` is a local Streamlit app for comparing how multiple Ollama models answer the same input.

`Ollama is required.` This repository does not include model execution by itself. You need a local Ollama installation and at least one installed model before this tool can work.

## 日本語

### 概要

`LLMCheckerNya` は、Ollama 上の複数モデルに同じ入力を与え、返答の違いをローカルで見比べる Streamlit アプリです。

### できること

- 1つの Ollama モデルに対して質問する
- 2つの Ollama モデルを並べて比較する
- 画像やスクリーンショットを添付したままプロンプトを送る
- システムプロンプトを画面から調整する

### 必須条件

- macOS
- Python 3.12
- Ollama アプリ本体がインストール済みで起動できること
- 比較に使う Ollama モデルが少なくとも 1 つインストール済みであること
- 画像比較を使う場合は Vision 対応モデルを少なくとも 1 つインストール済みであること

### 動作確認済みパッケージ

- `streamlit==1.50.0`
- `ollama==0.6.1`
- `pillow==11.3.0`

### セットアップ

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ollama 本体が未導入なら先にインストールし、モデルも取得してください。

例:

```bash
ollama pull gemma3
```

画像比較を使う場合は Vision 対応モデルを使ってください。

### 起動方法

方法1:

```bash
./run_llm_checker_nya.command
```

方法2:

```bash
source .venv/bin/activate
streamlit run app.py
```

### 使い方

1. サイドバーで使用するモデルを選ぶ
2. 必要なら比較モードを有効にする
3. 必要なら画像やスクリーンショットをアップロードする
4. 同じ質問をチャット欄に入力して、モデルごとの差分を見比べる

### 比較しやすい題材

- 同じ文章を要約させる
- 画像やスクリーンショットの説明をさせる
- 文章の言い換えや校正をさせる
- アイデア出しや観点出しをさせる

### 注意点

- このツール単体では動きません。Ollama 本体が必要です
- 回答品質は選択した Ollama モデルに依存します
- このアプリはローカル実行前提です。外部 API キーは使いません

## English

### Overview

`LLMCheckerNya` is a local Streamlit app for comparing how multiple Ollama models respond to the same prompt.

### What It Does

- Ask a single Ollama model
- Compare two Ollama models side by side
- Send prompts with optional images or screenshots
- Adjust the system prompt from the UI

### Requirements

- macOS
- Python 3.12
- A working local Ollama installation
- At least one installed Ollama model
- At least one vision-capable model if you want to compare image inputs

### Verified Packages

- `streamlit==1.50.0`
- `ollama==0.6.1`
- `pillow==11.3.0`

### Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If Ollama is not installed yet, install it first and pull at least one model.

Example:

```bash
ollama pull gemma3
```

Use a vision-capable model if you want to compare image inputs.

### Run

Option 1:

```bash
./run_llm_checker_nya.command
```

Option 2:

```bash
source .venv/bin/activate
streamlit run app.py
```

### Usage

1. Select the model(s) from the sidebar
2. Enable compare mode if needed
3. Optionally upload an image or screenshot
4. Submit the same prompt and compare the responses

### Good Comparison Prompts

- Summarizing the same text
- Describing the same image or screenshot
- Rewriting or proofreading a sentence
- Brainstorming ideas or perspectives

### Notes

- This tool does not run models by itself. Ollama is required
- Response quality depends on the selected Ollama model
- This app is designed for local use and does not require external API keys

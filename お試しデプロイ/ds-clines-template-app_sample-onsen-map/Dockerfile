# Python 3.12のslimイメージを使用
FROM python:3.13-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新と必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install poetry

# Poetryの設定（仮想環境を作成しない）
RUN poetry config virtualenvs.create false

# 依存関係ファイルとREADMEをコピー
COPY pyproject.toml poetry.lock* README.md ./

# 依存関係のインストール
RUN poetry install --only=main --no-root --no-interaction --no-ansi

# アプリケーションファイルをコピー
COPY src/ ./src/
COPY data/ ./data/

# ポート8501を公開
EXPOSE 8501

# ヘルスチェック
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Streamlitアプリケーションを起動
CMD ["streamlit", "run", "src/app_main.py", "--server.port=8501", "--server.address=0.0.0.0"]

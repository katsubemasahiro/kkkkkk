# テクニカルコンテキスト

## 開発環境
- **Python**: 3.9
- **パッケージ管理**: Poetry
- **エディタ**: Visual Studio Code
- **バージョン管理**: Git

## 主要依存関係
- **Webアプリケーション**: Streamlit (v1.50.0)
- **データ処理**: Pandas (v2.3.2)
- **地図表示**: Folium (v0.20.0)
- **地図連携**: streamlit-folium (v0.25.2)
- **データ収集**: Requests (v2.32.5), BeautifulSoup4 (v4.13.5)
- **位置情報**: Geocoder (v1.38.1)
- **その他**: NumPy, Pillow, JSON, CSV

## 開発セットアップ
```bash
# プロジェクト初期化
poetry init --no-interaction --name "onsen-map" --description "日本100名泉をマップに表示するアプリ" --author "Cline" --python ">=3.9,!=3.9.7,<4.0"

# 依存関係インストール
poetry add streamlit pandas folium streamlit-folium requests beautifulsoup4 geocoder

# 開発用依存関係
poetry add --dev pytest black isort
```

## プロジェクト構造
```
onsen-map/
├── pyproject.toml     # Poetryプロジェクト設定
├── README.md          # プロジェクト説明
├── data/              # データディレクトリ
│   └── images/        # 画像ディレクトリ
├── src/               # ソースコード
│   ├── app.py          # メインアプリケーション
│   ├── data_collector.py # データ収集モジュール
│   ├── data_loader.py  # データ読み込みモジュール
│   └── map_view.py     # マップ表示機能
└── tests/             # テストコード
```

## デプロイメント
- **ローカル実行**: `cd onsen-map/src && poetry run streamlit run app.py`
- **クラウドデプロイ**: Streamlit Cloud または Heroku
  - Streamlit Cloudへのデプロイには、GitHubリポジトリ連携が最適
  - Herokuの場合は`Procfile`を追加: `web: cd src && streamlit run app.py`

## 実行フロー
1. アプリを起動（`streamlit run src/app.py`）
2. サイドバーの「データを収集する」ボタンをクリック
3. Wikipediaからのデータ収集と位置情報取得が実行される
4. マップとデータテーブルに結果が表示される

## テクニカル制約
- 無料のAPIリクエスト制限を考慮したジオコーディング（OpenStreetMap API）
- 静的データ使用によるリアルタイム情報の限界
- Wikipediaのスクレイピング精度（HTML構造に依存）
- Streamlitの制約（ページナビゲーションなど）
- マーカークラスタリング表示時のパフォーマンス（大量データ時）

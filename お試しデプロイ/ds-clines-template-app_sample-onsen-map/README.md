## Clineによるアプリ開発のためのツールセット

### 概要
このリポジトリでは、Clineを使った効率的なアプリ開発のためのテンプレートを提供する

### クイックスタート
1. このリポジトリをクローン
2. Custom Instrunctionに[これ](https://docs.cline.bot/prompting/cline-memory-bank#cline-memory-bank-custom-instructions-%5Bcopy-this%5D)をコピペ
3. 共通ルールを設定:`clinerules-bank/common`フォルダ内のルール定義ファイルを`.clinerules`にコピー
4. 仕様書等を格納する または Planモードでやりたいことを決定する
5. Clineで「initialize memory bank」を実行
6. 開発開始！


### フォルダ構成

```
ds-clines-template/
├── .clinerules/               # プロジェクトルール設定フォルダ
│   └── .keep                      # Gitリポジトリに空フォルダを含めるためのファイル
│
├── clinerules-bank/           # Clineルール事例集
│   ├── common/                # 共通のルール定義
│   │   ├── 01-tech-stack.md       # 使用する技術スタックとバージョン情報
│   │   ├── 02-coding.md           # コーディング規約
│   │   ├── 03-documentation.md    # ドキュメンテーション規約
│   │   └── 04-workflow-guidelines.md # ワークフロー・ガイドライン
│   │
│   └── project-specific/      # プロジェクト固有のルール定義
│       └── .keep                  # Gitリポジトリに空フォルダを含めるためのファイル
│
├── memory-bank/               # Clineのメモリーバンク（プロジェクト記憶）
│   └── .keep                      # Gitリポジトリに空フォルダを含めるためのファイル
│
└── README.md                  # プロジェクト概要
```

### 環境設定方法

プロジェクトを開始するには、以下の手順で環境を設定してください：

1. **共通ルールの設定**：
   `clinerules-bank/common` フォルダ内のルール定義ファイルを `.clinerules` フォルダにコピーします。

2. **プロジェクト固有ルールの設定**：
   必要に応じて、プロジェクトに適したルールファイルを `clinerules-bank/project-specific` フォルダにコピーします。

#### セットアップコマンド

**Linux / macOS:**
```bash
# 共通ルールをコピー
cp clinerules-bank/common/* .clinerules/

# プロジェクト固有ルールがある場合は適宜コピー
# 例: cp path/to/project-rules/* clinerules-bank/project-specific/
```

**Windows (CMD):**
```cmd
rem 共通ルールをコピー
copy clinerules-bank\common\* .clinerules\

rem プロジェクト固有ルールがある場合は適宜コピー
rem 例: copy path\to\project-rules\* clinerules-bank\project-specific\
```

**Windows (PowerShell):**
```powershell
# 共通ルールをコピー
Copy-Item -Path clinerules-bank\common\* -Destination .clinerules

# プロジェクト固有ルールがある場合は適宜コピー
# 例: Copy-Item -Path path\to\project-rules\* -Destination clinerules-bank\project-specific
```


### Memory Bankについて
Memory Bankは、Clineがタスクを跨いだときに記憶喪失にならないようにする仕組み  
`memory-bank`フォルダ下のファイルを読み書きすることにより、Clineは一度リセットされても、プロジェクトの状況を理解して継続的に作業できるようになる  
参考：https://docs.cline.bot/prompting/cline-memory-bank

**Custom Instructionの設定**  
Clineの設定画面の下部にCustom Instructionの入力欄がある。
そちらに[これ](https://docs.cline.bot/prompting/cline-memory-bank#cline-memory-bank-custom-instructions-%5Bcopy-this%5D)をコピペ

**Memory Bankのつかいかた**  
以下の三つを主に使用する
 - **“initialize memory bank”**  
Memory Bankの初期化 新しいプロジェクトを開始する際に使用
 - **“follow your custom instructions”**  
 カスタム指示を読む ClineがMemory Bankファイルを読み、中断したところから継続（タスクの開始時に使用）
 - **“update memory bank”**  
 Memory Bankの更新 タスク中にドキュメントを更新したくなった時

### .clineignoreについて
Clineに読まれたくない機密データ等がある場合、`.clineignore`に以下のように指定する。

```
# Dependencies
node_modules/
**/node_modules/
.pnp
.pnp.js

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Large data files
*.csv
*.xlsx
```

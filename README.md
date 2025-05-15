# NinaPro ZIP Downloader & Extractor

このPythonスクリプトは、NinaProデータベースの各データセット（DB1〜DB10）に対応したウェブページからZIPファイルを自動でダウンロードし、解凍・整理を行います。

## 機能

- NinaProの各DBページからZIPファイルのリンクを自動検出
- ZIPファイルの順次ダウンロード
- ダウンロードしたZIPファイルを指定フォルダに解凍
- 各DBの中のサブフォルダ（例：s1, s2, ...）から `.mat` ファイルを一箇所にまとめてコピー

## 動作環境

- Python 3.x
- 以下のPythonパッケージが必要
  - `requests`
  - `beautifulsoup4`

```bash
pip install requests beautifulsoup4
```

## 使い方

1. スクリプトを任意のPython環境に保存します（例：`download_ninapro.py`）。
2. 実行すると、ユーザーのデスクトップ上に `NinaPro_Zips` フォルダが作成され、その中に `DB1` 〜 `DB10` のフォルダが作られます。
3. 各DBフォルダ内にZIPファイルがダウンロードされ、解凍されます。
4. 各DBフォルダ内のサブフォルダ（s1, s2, ...）にある `.mat` ファイルが `all_mat` フォルダにまとめられます。

```bash
python download_ninapro.py
```

## フォルダ構成例

```
NinaPro_Zips/
└── DB1/
    ├── ZIPファイル1.zip
    ├── ZIPファイル1/
    │   ├── s1/
    │   │   └── xxx.mat
    │   └── s2/
    │       └── yyy.mat
    ├── all_mat/
    │   ├── xxx.mat
    │   └── yyy.mat
    └── ...
```

## 注意事項

- ネットワークの状態やサーバーの応答により、ダウンロードに失敗する場合があります。
- ダウンロード/解凍の失敗はエラーメッセージとして表示されます。
- スクリプトは既存のファイルを上書きする場合がありますのでご注意ください。（同じ名前のフォルダーがある場合）


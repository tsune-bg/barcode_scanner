# バーコードスキャナー

アップロードされた画像からバーコードをスキャンして製品情報を表示するアプリケーション

## 使い方

1. アプリケーションを実行
2. バーコードが含まれる画像をアップロードしスキャンを開始
3. 製品情報が表示される

## ファイル構成

```
.
├── app.py
├── product_database.py
├── barcode_scanner.py
├── templates
│   └── index.html
│   └── base.html
└── static
    ├── css
    │   └── custom.css
    └── js
        └── main.js
```

`app.py`: アプリケーションのエントリーポイント
`templates/`: HTMLテンプレート
`static/`: CSSやJavaScriptなどの静的ファイル

## 開発

### 環境変数の設定

1. [JANCODE LOOKUP](https://www.jancodelookup.com/) からアプリ ID を発行
2. `.env` を `.env.example` から作成し、`JANCODE_API_KEY` にアプリ ID を記入

### Docker での起動

1.  Docker イメージをビルド: `docker build -t barcode_scanner .`
2.  Docker コンテナを実行: `docker run -p 5001:5001 barcode_scanner`
3.  アプリケーションをブラウザで開く: `http://localhost:5001`

## ライセンス

MIT license

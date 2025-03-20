# バーコードスキャナー

このプロジェクトは、バーコードをスキャンして製品情報を表示するアプリケーションです

## 使い方

1. アプリケーションを実行
2. バーコードスキャナーを使用して製品のバーコードをスキャンする
3. 製品情報が表示される

## ファイル構成

```
.
├── app.py
├── product_database.py
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
`product_database.py`: 製品データベースを管理
`templates/`: HTMLテンプレート
`static/`: CSSやJavaScriptなどの静的ファイル

## 開発



### Docker での起動

1.  Docker イメージをビルドします: `docker build -t barcode_scanner .`
2.  Docker コンテナを実行します: `docker run -p 5001:5001 barcode_scanner`
3.  アプリケーションをブラウザで開きます: `http://localhost:5001`


## ライセンス

MIT

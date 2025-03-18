import logging
import os
import requests
import json

logger = logging.getLogger(__name__)

# フォールバック用の内部データベース（APIが利用できない場合に使用）
FALLBACK_DATABASE = {
    # EAN-13 Sample Products
    "4901777046504": {
        "name": "Pocky Chocolate",
        "manufacturer": "Glico",
        "category": "Snacks",
        "description": "Chocolate-coated biscuit sticks"
    },
    "4901201126796": {
        "name": "Curry Rice",
        "manufacturer": "House Foods",
        "category": "Ready Meals",
        "description": "Japanese curry with rice"
    },
    # 他の商品は省略
}

def get_product_from_api(barcode):
    """
    JAN Code Lookup APIから商品情報を取得する
    
    Args:
        barcode (str): 検索するバーコード番号
        
    Returns:
        dict: 商品情報またはNone（見つからない場合）
    """
    api_key = os.environ.get("JANCODE_API_KEY")
    if not api_key:
        logger.error("JAN Code APIキーが設定されていません")
        return None
        
    # バーコードが短すぎる場合はスキップ
    if len(barcode) < 8:
        logger.error(f"バーコード番号が短すぎます: {barcode}")
        return None
    
    # APIエンドポイント（ドキュメント通り）
    api_url = "https://api.jancodelookup.com/"
    
    # リクエストヘッダー
    headers = {
        "Accept": "application/json"
    }
    
    # リクエストパラメータ（ドキュメント通り）
    params = {
        "appId": api_key,    # アプリID（必須）
        "query": barcode,    # 検索キーワード（必須）
        "type": "code",      # 検索タイプ：コード番号限定検索
        "hits": 1            # 取得件数（1件だけ取得）
    }
    
    try:
        logger.debug(f"APIリクエスト: {api_url} パラメータ:{params} ヘッダー:{headers}")
        response = requests.get(api_url, headers=headers, params=params)
        
        # レスポンスのステータスコードをチェック
        if response.status_code == 200:
            data = response.json()
            logger.debug(f"API応答: {json.dumps(data, indent=2)}")
            
            # JANコード検索APIのレスポンス形式に合わせて結果を処理
            if data and isinstance(data, dict):
                # ヒット件数をチェック
                if data.get("hits") > 0 and "items" in data and isinstance(data["items"], list) and data["items"]:
                    # 最初の商品情報を取得
                    item = data["items"][0]
                    
                    # 必要なフォーマットに変換
                    result = {
                        "name": item.get("name", "不明"),
                        "manufacturer": item.get("manufacturer", item.get("maker", "不明")),
                        "category": item.get("category", "不明"),
                        "description": item.get("description", item.get("abstract", "説明なし"))
                    }
                    logger.debug(f"商品情報: {result}")
                    return result
            
            logger.debug(f"商品情報の抽出に失敗しました: {data}")
            return None
        else:
            logger.error(f"API エラー: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"API リクエスト中にエラーが発生しました: {str(e)}")
        return None

def get_product_by_barcode(barcode):
    """
    バーコード番号から商品情報を検索する
    
    Args:
        barcode (str): 検索するバーコード番号
        
    Returns:
        dict: 商品情報またはNone（見つからない場合）
    """
    # バーコードをクリーンアップ（数字以外の文字を削除）
    cleaned_barcode = ''.join(filter(str.isdigit, barcode))
    
    logger.debug(f"バーコードで商品を検索: {cleaned_barcode}")
    
    # まずAPIから商品情報を取得
    product = get_product_from_api(cleaned_barcode)
    
    # API経由で商品が見つかった場合
    if product:
        logger.debug(f"API経由で商品が見つかりました: {product}")
        return product
    
    # APIで見つからなかった場合はフォールバックデータベースを確認
    product = FALLBACK_DATABASE.get(cleaned_barcode)
    if product:
        logger.debug(f"ローカルデータベースで商品が見つかりました: {product}")
        return product
    
    # どちらにも見つからなかった場合
    logger.debug(f"商品が見つかりませんでした: {cleaned_barcode}")
    return None

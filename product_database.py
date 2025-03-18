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
    
    # APIエンドポイント
    api_url = f"https://api.jancodelookup.com/v2/products/{barcode}"
    
    # リクエストヘッダー
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    try:
        logger.debug(f"APIリクエスト: {api_url}")
        response = requests.get(api_url, headers=headers)
        
        # レスポンスのステータスコードをチェック
        if response.status_code == 200:
            data = response.json()
            logger.debug(f"API応答: {json.dumps(data, indent=2)}")
            
            # 商品が見つかった場合
            if data.get("success") and data.get("products"):
                product = data["products"][0]  # 最初の結果を使用
                
                # 必要なフォーマットに変換
                result = {
                    "name": product.get("name", "不明"),
                    "manufacturer": product.get("brand", {}).get("name", "不明"),
                    "category": product.get("category", {}).get("name", "不明"),
                    "description": product.get("description", "説明なし")
                }
                logger.debug(f"商品情報: {result}")
                return result
            else:
                logger.debug(f"商品が見つかりませんでした: {data}")
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

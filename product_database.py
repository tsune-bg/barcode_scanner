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
    
    # APIエンドポイント
    api_url = "https://api.jancodelookup.com/v2/products"
    
    # リクエストヘッダー
    headers = {
        "Accept": "application/json"
    }
    
    # リクエストパラメータ
    params = {
        "jan": barcode,
        "appId": api_key  # APIドキュメントによるとappIdパラメータが必要
    }
    
    try:
        logger.debug(f"APIリクエスト: {api_url} パラメータ:{params} ヘッダー:{headers}")
        response = requests.get(api_url, headers=headers, params=params)
        
        # レスポンスのステータスコードをチェック
        if response.status_code == 200:
            data = response.json()
            logger.debug(f"API応答: {json.dumps(data, indent=2)}")
            
            # レスポンスから商品情報を抽出（APIの実際のレスポンス形式に合わせて調整）
            # ここでは汎用的なアプローチを取る
            if data and isinstance(data, dict):
                # 商品データの抽出を試みる（APIによって異なる可能性がある）
                product_data = None
                
                # レスポンスが異なる構造である可能性がある
                if "products" in data and isinstance(data["products"], list) and data["products"]:
                    product_data = data["products"][0]
                elif "product" in data:
                    product_data = data["product"]
                elif "item" in data:
                    product_data = data["item"]
                else:
                    # データに製品情報が含まれていると仮定
                    product_data = data
                
                if product_data:
                    # 必要なフォーマットに変換（フィールド名はAPIによって異なる可能性がある）
                    result = {
                        "name": product_data.get("name", product_data.get("product_name", "不明")),
                        "manufacturer": product_data.get("manufacturer", 
                                      product_data.get("brand", {}).get("name", "不明") if isinstance(product_data.get("brand"), dict) else 
                                      product_data.get("brand", "不明")),
                        "category": product_data.get("category", 
                                 product_data.get("category", {}).get("name", "不明") if isinstance(product_data.get("category"), dict) else
                                 "不明"),
                        "description": product_data.get("description", product_data.get("details", "説明なし"))
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

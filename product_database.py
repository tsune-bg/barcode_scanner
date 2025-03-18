import logging

logger = logging.getLogger(__name__)

# In-memory product database for MVP
# In a real application, this would be replaced with a database or external API
PRODUCT_DATABASE = {
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
    "4902102072618": {
        "name": "Kirin Afternoon Tea",
        "manufacturer": "Kirin Beverage",
        "category": "Beverages",
        "description": "Bottled milk tea"
    },
    "4902220157006": {
        "name": "Cup Noodle (Original)",
        "manufacturer": "Nissin",
        "category": "Instant Food",
        "description": "Instant ramen in a cup"
    },
    
    # UPC-A Sample Products
    "049000006346": {
        "name": "Coca-Cola Classic",
        "manufacturer": "Coca-Cola Company",
        "category": "Beverages",
        "description": "Classic cola soft drink"
    },
    "021130126026": {
        "name": "Doritos Nacho Cheese",
        "manufacturer": "Frito-Lay",
        "category": "Snacks",
        "description": "Nacho cheese flavored tortilla chips"
    },
    "038000138416": {
        "name": "Cheerios",
        "manufacturer": "General Mills",
        "category": "Breakfast Cereal",
        "description": "Whole grain oat cereal"
    },
    
    # Add more sample products as needed
    "9780201379624": {
        "name": "Design Patterns",
        "manufacturer": "Addison-Wesley",
        "category": "Books",
        "description": "Elements of Reusable Object-Oriented Software"
    }
}

def get_product_by_barcode(barcode):
    """
    Look up product information by barcode number
    
    Args:
        barcode (str): The barcode number to look up
        
    Returns:
        dict: Product information or None if not found
    """
    # Clean up the barcode - remove any non-numeric characters that might be present
    cleaned_barcode = ''.join(filter(str.isdigit, barcode))
    
    logger.debug(f"Looking up product for barcode: {cleaned_barcode}")
    
    # Look up the product in our database
    product = PRODUCT_DATABASE.get(cleaned_barcode)
    
    if product:
        logger.debug(f"Product found: {product}")
        return product
    else:
        logger.debug(f"No product found for barcode: {cleaned_barcode}")
        return None

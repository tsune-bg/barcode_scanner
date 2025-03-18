import cv2
from pyzbar.pyzbar import decode
import logging

logger = logging.getLogger(__name__)

def scan_barcode(image_path):
    """
    Scan and decode barcode from an image file
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        dict: Dictionary containing barcode data and type, or None if no barcode found
    """
    try:
        # Read the image
        image = cv2.imread(image_path)
        
        if image is None:
            logger.error(f"Could not read image from {image_path}")
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply some image processing to improve barcode detection
        # Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Try to decode barcode from the original grayscale image
        barcodes = decode(gray)
        
        # If no barcode found, try with the processed image
        if not barcodes:
            barcodes = decode(thresh)
        
        # If still no barcode found, try with the original image
        if not barcodes:
            barcodes = decode(image)
        
        # No barcode detected
        if not barcodes:
            logger.warning("No barcode detected in the image")
            return None
        
        # Get the first barcode found
        barcode = barcodes[0]
        
        # Extract barcode data
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        
        logger.debug(f"Barcode detected: {barcode_data} ({barcode_type})")
        
        return {
            'data': barcode_data,
            'type': barcode_type
        }
        
    except Exception as e:
        logger.error(f"Error scanning barcode: {str(e)}")
        return None

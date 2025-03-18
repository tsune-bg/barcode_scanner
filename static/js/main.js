document.addEventListener('DOMContentLoaded', function() {
    const barcodeForm = document.getElementById('barcode-form');
    const scanButton = document.getElementById('scan-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const resultContainer = document.getElementById('result-container');
    
    // Barcode result elements
    const barcodeNumber = document.getElementById('barcode-number');
    const barcodeType = document.getElementById('barcode-type');
    
    // Product information elements
    const productName = document.getElementById('product-name');
    const productManufacturer = document.getElementById('product-manufacturer');
    const productCategory = document.getElementById('product-category');
    const productDescription = document.getElementById('product-description');
    
    barcodeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading indicator and hide previous results/errors
        loadingIndicator.classList.remove('d-none');
        errorMessage.classList.add('d-none');
        resultContainer.classList.add('d-none');
        scanButton.disabled = true;
        
        // Get the file input
        const fileInput = document.getElementById('image-upload');
        const file = fileInput.files[0];
        
        if (!file) {
            showError('Please select an image file');
            return;
        }
        
        // Create FormData object
        const formData = new FormData();
        formData.append('image', file);
        
        try {
            // Send the image to the server for processing
            const response = await fetch('/scan', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'An unknown error occurred');
            }
            
            // Update the UI with the scan results
            displayResults(data);
            
        } catch (error) {
            showError(error.message || 'Failed to process the image');
        } finally {
            // Hide loading indicator and re-enable button
            loadingIndicator.classList.add('d-none');
            scanButton.disabled = false;
        }
    });
    
    function displayResults(data) {
        // Display barcode information
        barcodeNumber.textContent = data.barcode;
        barcodeType.textContent = data.type;
        
        // Always show the barcode information section
        resultContainer.classList.remove('d-none');
        
        if (data.product) {
            // Display product information
            productName.textContent = data.product.name || 'N/A';
            productManufacturer.textContent = data.product.manufacturer || 'N/A';
            productCategory.textContent = data.product.category || 'N/A';
            productDescription.textContent = data.product.description || 'N/A';
        } else {
            // Show empty values for product information
            productName.textContent = '商品情報なし';
            productManufacturer.textContent = '商品情報なし';
            productCategory.textContent = '商品情報なし';
            productDescription.textContent = '商品情報なし';
            
            // Add a note about missing product info (optional)
            errorText.textContent = 'このバーコードに一致する商品情報がデータベースに見つかりませんでした。';
            errorMessage.classList.remove('d-none');
        }
    }
    
    function showError(message) {
        errorText.textContent = message;
        errorMessage.classList.remove('d-none');
        loadingIndicator.classList.add('d-none');
    }
    
    // Preview the selected image (optional enhancement)
    const imageUpload = document.getElementById('image-upload');
    
    imageUpload.addEventListener('change', function() {
        // Reset any previous results or errors when a new file is selected
        errorMessage.classList.add('d-none');
        resultContainer.classList.add('d-none');
    });
});

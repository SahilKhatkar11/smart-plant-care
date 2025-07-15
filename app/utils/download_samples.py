import os
import requests
from PIL import Image
from io import BytesIO

def download_image(url, save_path):
    try:
        print(f"Downloading {url}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, verify=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        print(f"Content type: {response.headers.get('content-type')}")
        print(f"Content length: {len(response.content)} bytes")
        
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        
        print(f"Image format: {img.format}")
        print(f"Image size: {img.size}")
        print(f"Image mode: {img.mode}")
        
        img = img.convert('RGB')  # Convert to RGB format
        img = img.resize((224, 224))  # Resize to our model's input size
        img.save(save_path)
        print(f"Successfully saved to {save_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Network error downloading {url}: {str(e)}")
        return False
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return False

# Sample image URLs with reliable sources
sample_images = {
    'healthy': [
        'https://images.pexels.com/photos/1458694/pexels-photo-1458694.jpeg',  # Healthy tomato plant
        'https://images.pexels.com/photos/1751682/pexels-photo-1751682.jpeg',  # Healthy tomato plant with fruits
        'https://images.pexels.com/photos/2886937/pexels-photo-2886937.jpeg'   # Healthy tomato plant in garden
    ],
    'unhealthy': [
        'https://images.pexels.com/photos/6231990/pexels-photo-6231990.jpeg',  # Damaged plant
        'https://images.pexels.com/photos/7728088/pexels-photo-7728088.jpeg',  # Diseased leaves
        'https://images.pexels.com/photos/7728089/pexels-photo-7728089.jpeg'   # Wilted plant
    ]
}

def main():
    # Create directories if they don't exist
    for category in ['healthy', 'unhealthy']:
        os.makedirs(f'data/{category}', exist_ok=True)
        print(f"\nProcessing {category} images...")
        
        # Download images for each category
        for i, url in enumerate(sample_images[category]):
            save_path = f'data/{category}/sample_{i+1}.jpg'
            if download_image(url, save_path):
                print(f"Successfully downloaded {save_path}")
            else:
                print(f"Failed to download image {i+1} for {category}")

if __name__ == "__main__":
    main() 
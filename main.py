import csv
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()

# Get the service account file path from the environment variables
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

# Load CSV file and watermark images
csv_file = 'input/input.csv'
image_urls = []
with open(csv_file, 'r', encoding='utf-8-sig') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        # Extract the URL from the quoted text
        image_url = row[0].split(';')[-1].split('"')[1]
        image_urls.append(image_url)

left_bottom_watermark_path = 'input/watermark1.png'
main_image_path = 'input/main.png'
desired_width = 1400
desired_height = 933

# Set up Google Drive API credentials and service
SCOPES = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)

# Output CSV file for storing image URLs
output_csv_file = 'output/watermarked_images.csv'

# Loop through image URLs and add watermarks
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Original Image URL', 'Watermarked Image URL'])

    for image_url in image_urls:
        try:
            # Download original image from URL
            response = requests.get(image_url)
            original_image = Image.open(BytesIO(response.content)).convert('RGBA')

            # Resize original image to desired dimensions
            original_image = original_image.resize((desired_width, desired_height))

            # Open watermark images and convert to RGBA mode
            left_bottom_watermark = Image.open(left_bottom_watermark_path).convert('RGBA')
            main_image = Image.open(main_image_path).convert('RGBA')

            # Calculate positions for watermarks
            main_width, main_height = main_image.size
            left_bottom_position = (0, main_height - left_bottom_watermark.height - 10)  # 10 pixels from the bottom
            original_position = ((main_width - desired_width) // 2, (main_height - desired_height) // 2)

            # Paste watermarks on the main image
            main_image.paste(original_image, original_position, original_image)
            main_image.paste(left_bottom_watermark, left_bottom_position, left_bottom_watermark)

            # Convert image to RGB mode before saving as JPEG
            main_image = main_image.convert('RGB')

            # Save the final image
            output_path = 'output/' + f'watermarked_{image_url.split("/")[-1]}.jpg'
            main_image.save(output_path)
            print(f'Watermarked image saved: {output_path}')

            # Upload the watermarked image to Google Drive
            media = MediaIoBaseUpload(BytesIO(main_image.tobytes()), mimetype='image/jpeg')
            file_metadata = {
                'name': f'watermarked_{image_url.split("/")[-1]}.jpg',
                'parents': ['<Your Google Drive Folder ID>'],  # Replace with your Google Drive folder ID
            }
            uploaded_file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink'
            ).execute()

            # Store the original and watermarked image URLs in the CSV file
            original_image_url = image_url
            watermarked_image_url = uploaded_file.get('webViewLink')
            csv_writer.writerow([original_image_url, watermarked_image_url])
            print(f'Watermarked image uploaded to Google Drive: {watermarked_image_url}')

        except Exception as e:
            print(f'Error processing {image_url}: {e}')

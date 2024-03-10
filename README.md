# Watermark and Upload Images to Google Drive

This Python script processes a list of image URLs from a CSV file, adds watermarks to the images, resizes them, and then uploads the watermarked images to Google Drive. It also stores the original and watermarked image URLs in a CSV file.

## Video Preview

[![Video Preview](https://github.com/DevRex-0201/Project-Images/blob/main/video%20preview/Py-Image-Watermark-Uploader.png)](https://drive.google.com/file/d/1_0fjYa_iLsTgU3-D4LtjH4hobgMRv4bV/view?usp=drive_link)

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- Install required Python packages using `pip`:
  ```
  pip install requests Pillow google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv
  ```

## Configuration

1. **Service Account Credentials:**
   - Create a service account on the Google Cloud Platform and download the JSON credentials file.
   - Save the JSON credentials file to your project directory.
   
2. **Environment Variables:**
   - Create a `.env` file in your project directory.
   - Add the path to your service account JSON file in the `.env` file:
     ```
     SERVICE_ACCOUNT_FILE=/path/to/your/service-account.json
     ```

3. **Input Files:**
   - Place the input CSV file containing image URLs in the `input` directory.
   - Provide the paths for the main image (`main.png`) and the watermark image (`watermark1.png`) in the script.

## Usage

1. Run the script using the following command:
   ```
   python watermark_and_upload.py
   ```

2. The script will download images from the provided URLs, add watermarks, resize them, upload them to Google Drive, and store the URLs in `watermarked_images.csv` in the `output` directory.

## Additional Notes

- Make sure the input CSV file follows the specified format with image URLs enclosed in double quotes.
- Ensure the images for watermarking (`main.png` and `watermark1.png`) are placed in the `input` directory.
- Adjust the watermark position and other parameters in the script according to your requirements.

---

Feel free to customize the README file further based on your specific project needs.

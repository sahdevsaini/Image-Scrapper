from flask import Flask, render_template, request
import os
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/review', methods=['POST'])
def review():
    search_term = request.form['content']
    download_images(search_term, num_images=10)
    return "Images downloaded successfully!"

def download_images(query, num_images=10):
    # Encode the search query to include in the URL
    search_query = '+'.join(query.split())
    url = f"https://www.google.com/search?q={search_query}&tbm=isch"

    # Send a GET request to Google Images
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_links = []

        # Extract image URLs from the HTML response
        for img in soup.find_all('img'):
            img_url = img.get('src')
            if img_url and img_url.startswith('http'):
                image_links.append(img_url)

        # Download images
        folder_name = os.path.join('images', query.replace(' ', '_') + '_images')
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        count = 0
        for img_link in image_links:
            if count >= num_images:
                break

            try:
                img_data = requests.get(img_link, timeout=10).content
                file_extension = '.jpg'  # Force file extension to be .jpg
                file_name = f"{folder_name}/image_{count}{file_extension}"

                with open(file_name, 'wb') as img_file:
                    img_file.write(img_data)
                count += 1
                print(f"Downloaded image {count}")
            except Exception as e:
                print(f"Error downloading image: {e}")

    else:
        print("Failed to fetch images from Google.")

if __name__ == '__main__':
    app.run(debug=True)

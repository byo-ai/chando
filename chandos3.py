import os
import random
import requests
import time
from tqdm import tqdm

# Read in the URLs from the 1.txt file
with open('/home/user/Downloads/chandos/aveclescumplimentsduchef.txt', 'r') as f:
    url_list = [line.strip() for line in f]

# Read in the file names from the 2.txt file
with open('/home/user/Downloads/chandos/talent2.txt', 'r') as f:
    file_names = [line.strip() for line in f]

# Set the minimum and maximum waiting times (in seconds)
min_wait_time = 5
max_wait_time = 15

# Iterate over the URLs and file names, downloading and renaming the PDFs
for url, file_name in zip(url_list, file_names):
    # Check if the URL is for a PDF file
    if url.endswith('.pdf'):
        # Send a request to download the PDF
        response = requests.get(url, stream=True)

        # Check if the response is a PDF file
        if 'Content-Type' in response.headers and response.headers['Content-Type'] == 'application/pdf':
            # Save the PDF to a file
            with open(file_name, 'wb') as f:
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024  # 1 Kibibyte
                tqdm_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
                for data in response.iter_content(block_size):
                    f.write(data)
                    tqdm_bar.update(len(data))
                tqdm_bar.close()
            print(f"Successfully downloaded and renamed {file_name}")
        else:
            print(f"Skipping {url}: not a PDF file")
    else:
        print(f"Skipping {url}: not a PDF file")

    # Wait for a random time between the minimum and maximum waiting times
    wait_time = random.uniform(min_wait_time, max_wait_time)
    time.sleep(wait_time)

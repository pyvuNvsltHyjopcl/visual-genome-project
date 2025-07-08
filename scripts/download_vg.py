import os
import requests
import zipfile
from tqdm import tqdm
#
#
#def download_and_unzip(url, target_dir):
#    """
#    Downloads and extracts a zip file.
#    """
#    os.makedirs(target_dir, exist_ok=True)
#    filename = url.split('/')[-1]
#    zip_path = os.path.join(target_dir, filename)
#
#    if not os.path.exists(zip_path):
#        print(f"Downloading {filename}...")
#        try:
#            with requests.get(url, stream=True) as r:
#                r.raise_for_status()
#                total_size = int(r.headers.get('content-length', 0))
#                with tqdm(total=total_size, unit='iB', unit_scale=True) as pbar:
#                    with open(zip_path, 'wb') as f:
#                        for chunk in r.iter_content(chunk_size=8192):
#                            pbar.update(len(chunk))
#                            f.write(chunk)
#        except requests.exceptions.RequestException as e:
#            print(f"Error downloading {url}: {e}")
#            return
#    else:
#        print(f"{filename} already exists. Skipping download.")
#
#    print(f"Extracting {filename}...")
#    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#        zip_ref.extractall(target_dir)
#    print(f"Successfully extracted {filename}.")
#
#
#def verify_manual_downloads(target_dir):
#    """Checks for the presence of the manually downloaded image folders."""
#    print("\nVerifying manual downloads...")
#    image_folder_1 = os.path.join(target_dir, "VG_100K")
#    image_folder_2 = os.path.join(target_dir, "VG_100K_2")
#
#    path_1_exists = os.path.exists(image_folder_1)
#    path_2_exists = os.path.exists(image_folder_2)
#
#    if path_1_exists and path_2_exists:
#        print(" Success: Both 'VG_100K' and 'VG_100K_2' folders found.")
#        return True
#    else:
#        print(" Action Required: Image folders not found.")
#        if not path_1_exists:
#            print(f"  - Please download and place the 'VG_100K' folder in '{target_dir}'.")
#        if not path_2_exists:
#            print(f"  - Please download and place the 'VG_100K_2' folder in '{target_dir}'.")
#        print("  - Download from: https://www.kaggle.com/datasets/dannygarcia/visual-genome")
#        return False
#
#
#if __name__ == "__main__":
#    ANNOTATION_URLS = {
#        "annotations": "https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/image_data.json.zip",
#        "objects": "https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/objects.json.zip",
#    }
#
#    RAW_DATA_DIR = os.path.join("..", "data", "raw")
#
#    print("--- Starting Visual Genome Dataset Acquisition ---")
#
#    # Step 1: Automated download of small annotation files
#    print("\n[Phase 1: Fetching Annotation Files]")
#    download_and_unzip(ANNOTATION_URLS["annotations"], RAW_DATA_DIR)
#    download_and_unzip(ANNOTATION_URLS["objects"], RAW_DATA_DIR)
#
#    # Step 2: Verification of large, manually-downloaded image files
#    print("\n[Phase 2: Verifying Image Files]")
#    verify_manual_downloads(RAW_DATA_DIR)
#
#    print("\n--- Dataset acquisition process complete! ---")
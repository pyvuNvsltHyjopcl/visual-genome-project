import os
import pandas as pd
from datasets import load_dataset


def flatten_visual_genome(config):
    """
    Streams a subset of the Visual Genome dataset, flattens the nested object
    data with real-time logging, and saves it as a clean CSV file.
    """
    print("--- Starting Data Flattening Process with Real-time Logging ---")

    # Create the output directory if it doesn't exist
    os.makedirs(config["output_dir"], exist_ok=True)

    # 1. Load the dataset in streaming mode (removed the incorrect DownloadConfig)
    dataset = load_dataset(
        "visual_genome",
        "objects_v1.2.0",
        split='train',
        trust_remote_code=True,
        streaming=True,
    )
    print(f"Dataset loaded. Will process the first {config['images_to_process']} images...")

    # 2. Process images with a direct loop for better feedback
    flattened_data = []
    processed_count = 0

    for image_example in dataset:
        # --- Flatten the data for the current image ---
        image_id = image_example['image_id']
        for obj in image_example['objects']:
            flat_record = {
                'image_id': image_id,
                'image_url': image_example['url'],
                'image_width': image_example['width'],
                'image_height': image_example['height'],
                'object_id': obj['object_id'],
                'object_name': obj['names'][0] if obj['names'] else None,
                'x': obj['x'], 'y': obj['y'], 'w': obj['w'], 'h': obj['h'],
            }
            flattened_data.append(flat_record)

        processed_count += 1

        # --- Log progress for each processed image ---
        print(f"  [Log] Processed image #{processed_count} (ID: {image_id})")

        # --- Stop after reaching the desired number of images ---
        if processed_count >= config['images_to_process']:
            print(f"\nReached the limit of {config['images_to_process']} images.")
            break

    # 3. Convert to a DataFrame and save
    if not flattened_data:
        print("No data was processed. Exiting.")
        return

    output_path = os.path.join(config["output_dir"], "processed_objects_flat.csv")
    print(f"Saving {len(flattened_data)} total objects to {output_path}...")

    df = pd.DataFrame(flattened_data)
    df.to_csv(output_path, index=False)

    print("--- Data flattening complete! ---")

flatten_config = {
    "output_dir": os.path.join("..", "data", "processed"),
    "images_to_process": 20,
    "top_n_objects": 20  # -- Analyze the top 20 objects --
}

if __name__ == "__main__":
    #config = {
    #    "output_dir": os.path.join("..", "data", "processed"),
    #    "images_to_process": 20,
    #}
    flatten_visual_genome(flatten_config)
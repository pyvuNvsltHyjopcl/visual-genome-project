import os
import pandas as pd
from datasets import load_dataset
from itertools import islice


def preprocess_visual_genome(config):
    """
    Streams the dataset from Hugging Face,
    filters it with progress reporting,
    and saves a subset.
    """
    print("--- Starting Data Preprocessing using Streaming ---")

    os.makedirs(config["output_dir"], exist_ok=True)

    # 1. Load the dataset in streaming mode
    dataset = load_dataset(
        "visual_genome",
        "objects_v1.2.0",
        split='train',
        trust_remote_code=True,
        streaming=True
    )
    print("Dataset loaded in streaming mode. Starting search...")

    # 2. Define the filter function
    def is_valid_example(example):
        valid_dims = example['width'] >= config["min_width"] and example['height'] >= config["min_height"]
        num_objects = len(example['objects']) if example['objects'] else 0
        valid_objects = config["min_objects"] <= num_objects <= config["max_objects"]
        return valid_dims and valid_objects

    # 3. Iterate with a visible progress loop
    processed_examples = []
    # Set a limit on how many total examples to scan to avoid an infinite loop
    search_limit = 50000

    print(f"Scanning up to {search_limit} examples to find {config['subset_size']} that match your criteria...")

    for i, example in enumerate(dataset):
        # Print progress every 2000 examples scanned
        if (i + 1) % 10 == 0:
            print(f"  ...scanned {i + 1} examples, found {len(processed_examples)} valid ones so far...")

        # Check if the example meets our criteria
        if is_valid_example(example):
            processed_examples.append(example)

        # Stop if we have found enough examples
        if len(processed_examples) >= config['subset_size']:
            print(f"\nFound {config['subset_size']} matching examples after scanning {i + 1} total records.")
            break

        # Stop if we have scanned too many examples without finding enough
        if i + 1 >= search_limit:
            print(f"\nReached search limit of {search_limit} records.")
            break

    # 4. Save the results
    if not processed_examples:
        print("Could not find any examples matching the criteria within the search limit.")
        return

    output_path = os.path.join(config["output_dir"], "preprocessed_visual_genome_subset.csv")
    print(f"Saving the {len(processed_examples)} found examples to {output_path}...")

    processed_df = pd.DataFrame(processed_examples)
    processed_df.to_csv(output_path, index=False)

    print("--- Preprocessing complete! ---")


if __name__ == "__main__":
    config = {
        "output_dir": os.path.join("..", "data", "raw"),
        "subset_size": 1000,
        "min_width": 1,
        "min_height": 1,
        "min_objects": 1,
        "max_objects": 50
    }
    preprocess_visual_genome(config)
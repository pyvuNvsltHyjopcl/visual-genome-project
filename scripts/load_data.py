from datasets import load_dataset


def verify_dataset_access():
    """
    Uses the Hugging Face datasets library to access Visual Genome.
    """
    print("Accessing Visual Genome via the Hugging Face Hub...")

    try:
        #split name to 'train', as it's the only one available.
        dataset = load_dataset(
            "visual_genome",
            "objects_v1.2.0",
            split='train',
            streaming=True,
            trust_remote_code=True
        )

        # Get the first example from the stream
        example = next(iter(dataset))

        print("\n Success! Connection established and data is accessible.")
        print("Here is a sample record from the 'objects_v1.2.0' configuration:")

        # Display key information from the first example
        print(f"\n- Image ID: {example['image_id']}")
        print(f"- Image URL: {example['url']}")

        # Display the first object found in the image's annotations
        if example['objects']:
            first_object = example['objects'][0]
            print(f"- First Object ID: {first_object['object_id']}")
            print(f"- First Object Name: {first_object['names']}")
            print(
                f"- First Object BBox: [{first_object['x']}, {first_object['y']}, {first_object['w']}, {first_object['h']}]")

    except Exception as e:
        print(f"\n An error occurred while trying to access the dataset: {e}")


if __name__ == "__main__":
    verify_dataset_access()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def analyze_processed_data(config):
    """
    Performs a comprehensive analysis of the processed (flattened) dataset,
    generates visualizations, and saves a summary report using UTF-8 encoding.
    """
    print("--- Starting Redesigned Analysis on Processed Data ---")

    # --- 1. Setup and Load Data ---
    os.makedirs(config["report_dir"], exist_ok=True)

    try:
        df = pd.read_csv(config["input_csv"])
        print(f"Successfully loaded '{config['input_csv']}' with {len(df)} records.")
    except FileNotFoundError:
        print(f"Error: The file '{config['input_csv']}' was not found.")
        return

    # --- 2. Feature Engineering & Deeper Analysis ---
    df['bbox_area'] = df['w'] * df['h']
    df['aspect_ratio'] = df['w'] / df['h']

    report_lines = [f"# Data Quality Report: `{config['input_csv']}`\n"]
    report_lines.append(f"This report summarizes the analysis of **{len(df)} objects** from the processed dataset.\n")

    # --- 3. Completeness and Distribution Analysis ---
    report_lines.append("## 1. Data Completeness\n")
    if df.isnull().sum().sum() == 0:
        report_lines.append("- ✅ The dataset is fully complete with no missing values.\n")
    else:
        report_lines.append("- ⚠️ Missing values were found. Further cleaning may be needed.\n")
        report_lines.append(df.isnull().sum().to_string())

    # --- 4. Object Frequency Visualization ---
    report_lines.append("## 2. Object Frequency\n")
    plt.figure(figsize=(12, 8))
    top_n_objects = df['object_name'].value_counts().nlargest(config["top_n_objects"])
    sns.barplot(x=top_n_objects.values, y=top_n_objects.index, hue=top_n_objects.index, palette="viridis", legend=False)

    plt.title(f'Top {config["top_n_objects"]} Most Frequent Objects', fontsize=16)
    plt.xlabel('Frequency', fontsize=12)
    plt.ylabel('Object Name', fontsize=12)
    plt.tight_layout()
    plot_path = os.path.join(config["report_dir"], "object_frequency.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Generated and saved object frequency plot to '{plot_path}'.")
    report_lines.append(
        "The most common objects provide insight into the dataset's primary context (e.g., indoor office scenes).\n")
    report_lines.append(f"![Object Frequency Plot]({os.path.basename(plot_path)})\n")

    # --- 5. Bounding Box Analysis & Visualizations ---
    report_lines.append("## 3. Bounding Box Analysis\n")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    sns.histplot(df['bbox_area'], bins=50, kde=True, ax=axes[0], color="skyblue")
    axes[0].set_title('Distribution of Bounding Box Area')
    axes[0].set_xlabel('Area (pixels²)')
    axes[0].set_ylabel('Frequency')

    sns.histplot(df['aspect_ratio'], bins=50, kde=True, ax=axes[1], color="salmon")
    axes[1].set_title('Distribution of Bounding Box Aspect Ratio')
    axes[1].set_xlabel('Aspect Ratio (width/height)')
    axes[1].set_ylabel('Frequency')

    plt.tight_layout()
    bbox_plot_path = os.path.join(config["report_dir"], "bbox_distributions.png")
    plt.savefig(bbox_plot_path)
    plt.close()
    print(f"Generated and saved bounding box distribution plots to '{bbox_plot_path}'.")
    report_lines.append(
        "The distribution of bounding box sizes and shapes can highlight common object scales and potential outliers.\n")
    report_lines.append(f"![BBox Distributions Plot]({os.path.basename(bbox_plot_path)})\n")

    # --- 6.1. Save the Final Report ---
    report_path = os.path.join(config["report_dir"], "analysis_report.md")

    # --- 6.2. Ensure the report directory exists ---
    with open(report_path, 'w', encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"Successfully generated and saved analysis report to '{report_path}'.")
    print("\n--- Analysis Complete ---")


if __name__ == "__main__":
    config = {
        "input_csv": os.path.join("..", "data", "processed", "processed_objects_flat.csv"),
        "report_dir": os.path.join("..", "report"),  # -- A new folder to save the report and plots --
        "top_n_objects": 20  # -- Analyze the top 20 objects --
    }
    analyze_processed_data(config)
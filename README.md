# COCO to Roboflow

A tool for converting COCO format datasets to Roboflow format.

## Installation

```bash
pip install git+https://github.com/yourusername/coco-to-roboflow.git
```

Or for development:

```bash
git clone https://github.com/yourusername/coco-to-roboflow.git
cd coco-to-roboflow
pip install -e .
```

## Usage

### Basic Usage

```bash
coco-to-roboflow /path/to/coco/dataset /path/to/output/roboflow/dataset
```

This will create a Roboflow format dataset with the following structure:
```
dataset/
  ├── train/
  │   ├── images/
  │   │   ├── image1.jpg
  │   │   ├── image2.jpg
  │   │   └── ...
  │   └── _annotations.coco.json
  ├── valid/
  │   ├── images/
  │   │   ├── image3.jpg
  │   │   ├── image4.jpg
  │   │   └── ...
  │   └── _annotations.coco.json
  └── test/
      ├── images/
      │   ├── image5.jpg
      │   ├── image6.jpg
      │   └── ...
      └── _annotations.coco.json
```

### Additional Options

- `--images-dir`: Base directory for images if different from the input directory
- `--verbose`: Show detailed progress during conversion

## Input Format

The tool expects a COCO format dataset with the following structure:
```
input_dir/
  ├── train.json
  ├── val.json
  └── test.json
```

Each JSON file should follow the COCO annotation format with `images`, `annotations`, and `categories` arrays.

## Output Format

The tool generates a Roboflow-compatible dataset with:
- Separate directories for train, valid (renamed from val), and test splits
- Images copied to an 'images' subdirectory within each split
- COCO annotations saved as '_annotations.coco.json' in each split directory
- File paths in the JSON updated to reference the new image locations

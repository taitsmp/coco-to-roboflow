#!/usr/bin/env python3

import argparse
import json
import shutil
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def create_global_category_mapping(found_splits: List[Tuple[str, Path]]) -> Tuple[List[Dict], Dict[int, int]]:
    """Create a global mapping of category IDs to zero-based indices across all splits"""
    # Collect all categories from all splits
    all_categories = []
    for _, split_file in found_splits:
        if not split_file.exists():
            continue
        with open(split_file, 'r') as f:
            coco_data = json.load(f)
            all_categories.extend(coco_data['categories'])
    
    # Create name-based mapping to handle duplicates
    name_to_index = {}
    current_index = 0
    for cat in all_categories:
        if cat['name'] not in name_to_index:
            name_to_index[cat['name']] = current_index
            current_index += 1
    
    # Create mapping from original IDs to zero-based indices
    category_id_to_index = {cat['id']: name_to_index[cat['name']] for cat in all_categories}
    
    # Get unique categories (by name) for output
    unique_categories = []
    seen_names = set()
    for cat in sorted(all_categories, key=lambda x: category_id_to_index[x['id']]):
        if cat['name'] not in seen_names:
            unique_categories.append(cat)
            seen_names.add(cat['name'])
    
    return unique_categories, category_id_to_index

def process_split(
    coco_file: Path,
    output_dir: Path,
    split_name: str,
    source_dir: Path,
    category_id_to_index: Dict[int, int],
    verbose: bool = False
) -> Optional[Dict]:
    """
    Process a single data split (train/val/test)
    """
    if not coco_file.exists():
        print(f"Skipping {split_name} split - file not found: {coco_file}")
        return None
    
    print(f"\nProcessing {split_name} split...")
    
    # Load COCO annotations
    with open(coco_file, 'r') as f:
        coco_data = json.load(f)
    
    # Create output directories
    split_dir = output_dir / split_name
    images_dir = split_dir / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Track statistics
    total_images = len(coco_data['images'])
    processed_images = 0
    skipped_images = 0
    
    # Update category IDs in annotations
    for ann in coco_data['annotations']:
        ann['category_id'] = category_id_to_index[ann['category_id']]
    
    # Update category IDs in categories list
    for cat in coco_data['categories']:
        cat['id'] = category_id_to_index[cat['id']]
    
    # Process each image
    for img_data in coco_data['images']:
        # Copy image file
        img_filename = img_data['file_name']
        source_path = source_dir / img_filename
        if not source_path.exists():
            print(f"Warning: Source image not found: {source_path}")
            skipped_images += 1
            continue
            
        dest_path = images_dir / source_path.name
        shutil.copy2(source_path, dest_path)
        
        # Update file path in the JSON
        img_data['file_name'] = f"images/{source_path.name}"
        
        processed_images += 1
        if verbose and processed_images % 10 == 0:
            print(f"  Processed {processed_images}/{total_images} images...")
    
    # Write the updated COCO JSON to the output directory
    output_json_path = split_dir / '_annotations.coco.json'
    with open(output_json_path, 'w') as f:
        json.dump(coco_data, f, indent=2)
    
    print(f"Split: {split_name}")
    print(f"  Total images in annotations: {total_images}")
    print(f"  Successfully processed: {processed_images}")
    if skipped_images > 0:
        print(f"  Skipped (images not found): {skipped_images}")
    
    return coco_data

def main():
    parser = argparse.ArgumentParser(description='Convert COCO format to Roboflow format')
    parser.add_argument('input_dir', type=Path, help='Input directory containing COCO json files')
    parser.add_argument('output_dir', type=Path, help='Output directory for Roboflow format dataset')
    parser.add_argument('--images-dir', type=Path,
                      help='Base directory for images. Will be prepended to image paths from COCO json')
    parser.add_argument('--verbose', action='store_true', default=False,
                      help='Show detailed progress')
    
    args = parser.parse_args()
    
    # If images_dir is not specified, use input_dir
    image_base_dir = args.images_dir if args.images_dir else args.input_dir
    
    print(f"\nInput directory: {args.input_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Images directory: {image_base_dir}")
    
    # Verify input files exist
    train_file = args.input_dir / 'train.json'
    val_file = args.input_dir / 'val.json'
    test_file = args.input_dir / 'test.json'
    
    found_splits = []
    if train_file.exists():
        found_splits.append(('train', train_file))
    if val_file.exists():
        found_splits.append(('val', val_file))
    if test_file.exists():
        found_splits.append(('test', test_file))
    
    if not found_splits:
        print("Error: No split files (train.json, val.json, test.json) found in input directory")
        return
    
    print(f"\nFound split files: {[split[0] for split in found_splits]}")
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create global category mapping first
    categories, category_id_to_index = create_global_category_mapping(found_splits)
    
    # Process each split
    for split_name, split_file in found_splits:
        # For Roboflow, we need to rename 'val' to 'valid'
        output_split_name = 'valid' if split_name == 'val' else split_name
        
        process_split(
            split_file,
            args.output_dir,
            output_split_name,
            image_base_dir,
            category_id_to_index,
            verbose=args.verbose
        )
    
    print("\nConversion complete!")
    print(f"Dataset created at: {args.output_dir}")
    
    if categories:
        print("\nFinal Class Mapping Summary:")
        print("---------------------------")
        print("Roboflow ID | Original ID | Class Name")
        print("---------------------------")
        
        # Create a mapping of Roboflow index to all original IDs that map to it
        index_to_originals = {}
        
        # Collect categories from all splits
        for split_name, split_file in found_splits:
            with open(split_file, 'r') as f:
                split_data = json.load(f)
                for cat in split_data['categories']:
                    roboflow_idx = category_id_to_index[cat['id']]
                    if roboflow_idx not in index_to_originals:
                        index_to_originals[roboflow_idx] = set()
                    index_to_originals[roboflow_idx].add((cat['id'], cat['name']))
        
        # Print sorted by Roboflow index
        for roboflow_idx in sorted(index_to_originals.keys()):
            originals = sorted(index_to_originals[roboflow_idx])  # Convert set to sorted list
            # Print first one normally
            print(f"{roboflow_idx:10d} | {originals[0][0]:10d} | {originals[0][1]}")
            # Print any duplicates with same Roboflow ID
            for orig_id, name in originals[1:]:
                print(f"{' ':10s} | {orig_id:10d} | {name} (duplicate)")
        print("---------------------------")

if __name__ == '__main__':
    main()

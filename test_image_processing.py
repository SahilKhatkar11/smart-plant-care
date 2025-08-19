#!/usr/bin/env python3
"""Test script for image processing functionality in Smart Plant Care."""
import os
import sys
import argparse
import tempfile
from PIL import Image
import io
import numpy as np
import random

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our app modules
from app.utils.model_utils import load_image_multiple_methods, analyze_image
from app.utils.image_diagnostics import diagnose_image, repair_image

def create_test_images(output_dir):
    """Create a set of test images with different formats and characteristics."""
    print(f"Creating test images in {output_dir}...")

    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Test Case 1: Valid RGB PNG
    img1 = Image.new('RGB', (224, 224), color=(0, 150, 0))
    img1.save(os.path.join(output_dir, "valid_rgb.png"))

    # Test Case 2: Valid RGBA PNG
    img2 = Image.new('RGBA', (224, 224), color=(0, 150, 0, 255))
    img2.save(os.path.join(output_dir, "valid_rgba.png"))

    # Test Case 3: Valid JPG
    img3 = Image.new('RGB', (224, 224), color=(0, 150, 0))
    img3.save(os.path.join(output_dir, "valid.jpg"), quality=95)

    # Test Case 4: Low-quality JPG
    img4 = Image.new('RGB', (224, 224), color=(0, 150, 0))
    img4.save(os.path.join(output_dir, "low_quality.jpg"), quality=10)

    # Test Case 5: Zero-dimension image (corrupted)
    with open(os.path.join(output_dir, "zero_dimension.png"), 'wb') as f:
        # Create a minimal PNG header with zero dimensions
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\r')
        f.write(b'IHDR\x00\x00\x00\x00\x00\x00\x00\x00')
        f.write(b'\x08\x02\x00\x00\x00\xfc\x18\xed\xdc')

    # Test Case 6: Truncated file
    with open(os.path.join(output_dir, "truncated.png"), 'wb') as f:
        img6 = Image.new('RGB', (224, 224), color=(0, 150, 0))
        img6.save(f, format='PNG')
        # Get the current position
        pos = f.tell()
        # Truncate to half the size
        f.seek(pos // 2)
        f.truncate()

    # Test Case 7: Create a complex image with simulated plant features
    complex_img = Image.new('RGB', (224, 224), color=(240, 240, 240))
    # Draw some green leaf-like shapes
    for i in range(10):
        # Create green leaf areas
        x = random.randint(0, 224)
        y = random.randint(0, 224)
        radius = random.randint(20, 60)

        for dx in range(-radius, radius):
            for dy in range(-radius, radius):
                if dx*dx + dy*dy < radius*radius:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 224 and 0 <= ny < 224:
                        # Green with some variation
                        complex_img.putpixel((nx, ny), (
                            random.randint(0, 100),
                            random.randint(100, 200),
                            random.randint(0, 50)
                        ))

    complex_img.save(os.path.join(output_dir, "complex_plant.png"))

    # Test Case 8: Create an image with invalid header but valid data
    with open(os.path.join(output_dir, "valid.png"), 'rb') as src:
        with open(os.path.join(output_dir, "invalid_header.png"), 'wb') as dst:
            data = src.read()
            # Corrupt header but keep most data
            corrupted_data = b'X' * 10 + data[10:]
            dst.write(corrupted_data)

    # Test Case 9: Create a very large image
    large_img = Image.new('RGB', (2000, 2000), color=(0, 150, 0))
    large_img.save(os.path.join(output_dir, "large.png"))

    # Test Case 10: Create a very small image
    small_img = Image.new('RGB', (32, 32), color=(0, 150, 0))
    small_img.save(os.path.join(output_dir, "small.png"))

    print(f"Created 10 test images in {output_dir}")
    return output_dir

def test_image_loading(test_dir):
    """Test image loading functionality."""
    results = {}

    # Test each image in the directory
    for filename in os.listdir(test_dir):
        if not any(filename.endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
            continue

        file_path = os.path.join(test_dir, filename)
        print(f"\nTesting image loading for: {filename}")

        # Method 1: Test direct loading
        try:
            image = load_image_multiple_methods(file_path)
            if image is not None:
                print(f"✅ Successfully loaded {filename}")
                print(f"   Mode: {image.mode}, Size: {image.width}x{image.height}")
                results[filename] = True
            else:
                print(f"❌ Failed to load {filename}")
                results[filename] = False
        except Exception as e:
            print(f"❌ Error loading {filename}: {str(e)}")
            results[filename] = False

        # Method 2: Test diagnostic tool
        try:
            diagnostic = diagnose_image(file_path)
            print(f"📊 Diagnostics for {filename}:")
            print(f"   Format: {diagnostic.get('format', 'Unknown')}")
            print(f"   Valid: {diagnostic.get('valid', False)}")
            if diagnostic.get('issues'):
                print(f"   Issues: {len(diagnostic.get('issues'))} found")

            # If diagnostics failed but image is valid, there's a discrepancy
            if not diagnostic.get('valid') and results[filename]:
                print("⚠️ Warning: Image loads but diagnostics failed")
        except Exception as e:
            print(f"❌ Error running diagnostics on {filename}: {str(e)}")

        # Method 3: Test repair function on corrupted images
        if not results[filename]:
            try:
                repaired = repair_image(file_path)
                if repaired is not None:
                    print(f"🔧 Successfully repaired {filename}")
                    print(f"   Repaired Mode: {repaired.mode}, Size: {repaired.width}x{repaired.height}")
                    # Update results to indicate repair worked
                    results[filename] = "Repaired"
                else:
                    print(f"❌ Failed to repair {filename}")
            except Exception as e:
                print(f"❌ Error repairing {filename}: {str(e)}")

    # Print summary
    print("\n=== Image Loading Test Summary ===")
    success_count = sum(1 for result in results.values() if result)
    repair_count = sum(1 for result in results.values() if result == "Repaired")
    failure_count = sum(1 for result in results.values() if not result)

    print(f"Total images tested: {len(results)}")
    print(f"Successfully loaded: {success_count}")
    print(f"Repaired successfully: {repair_count}")
    print(f"Failed to load: {failure_count}")

    return results

def test_image_analysis(test_dir):
    """Test image analysis functionality."""
    results = {}

    # Test each image in the directory
    for filename in os.listdir(test_dir):
        if not any(filename.endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
            continue

        file_path = os.path.join(test_dir, filename)
        print(f"\nTesting image analysis for: {filename}")

        # First load the image
        try:
            image = load_image_multiple_methods(file_path)
            if image is None:
                print(f"❌ Cannot analyze {filename} - failed to load")
                results[filename] = "Load Failed"
                continue

            # Now analyze the image
            health_status, confidence = analyze_image(image)

            if health_status is not None and confidence is not None:
                print(f"✅ Successfully analyzed {filename}")
                print(f"   Health Status: {'Healthy' if health_status else 'Unhealthy'}")
                print(f"   Confidence: {confidence:.2f}")
                results[filename] = True
            else:
                print(f"❌ Analysis returned None for {filename}")
                results[filename] = False
        except Exception as e:
            print(f"❌ Error analyzing {filename}: {str(e)}")
            results[filename] = False

    # Print summary
    print("\n=== Image Analysis Test Summary ===")
    success_count = sum(1 for result in results.values() if result is True)
    failure_count = sum(1 for result in results.values() if result is False)
    load_failed = sum(1 for result in results.values() if result == "Load Failed")

    print(f"Total images tested: {len(results)}")
    print(f"Successfully analyzed: {success_count}")
    print(f"Analysis failed: {failure_count}")
    print(f"Loading failed (not analyzed): {load_failed}")

    return results

def run_full_test_suite(output_dir=None):
    """Run all tests in sequence."""
    # Create a temporary directory if none provided
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="plant_care_test_")

    # Create test images
    test_dir = create_test_images(output_dir)

    print("\n" + "="*50)
    print("RUNNING IMAGE LOADING TESTS")
    print("="*50)
    loading_results = test_image_loading(test_dir)

    print("\n" + "="*50)
    print("RUNNING IMAGE ANALYSIS TESTS")
    print("="*50)
    analysis_results = test_image_analysis(test_dir)

    print("\n" + "="*50)
    print("OVERALL TEST SUMMARY")
    print("="*50)

    success_loading = sum(1 for result in loading_results.values() if result)
    success_analysis = sum(1 for result in analysis_results.values() if result is True)

    print(f"Images tested: {len(loading_results)}")
    print(f"Loading success rate: {success_loading}/{len(loading_results)} ({success_loading/len(loading_results)*100:.1f}%)")
    print(f"Analysis success rate: {success_analysis}/{len(analysis_results)} ({success_analysis/len(analysis_results)*100:.1f}%)")

    return test_dir, loading_results, analysis_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test image processing functionality in Smart Plant Care")
    parser.add_argument("--output-dir", help="Directory to store test images (defaults to temp directory)")
    parser.add_argument("--test-type", choices=["all", "loading", "analysis"], default="all",
                        help="Type of test to run (default: all)")

    args = parser.parse_args()

    if args.test_type == "all":
        run_full_test_suite(args.output_dir)
    elif args.test_type == "loading":
        if args.output_dir and os.path.exists(args.output_dir):
            test_image_loading(args.output_dir)
        else:
            test_dir = create_test_images(args.output_dir or tempfile.mkdtemp(prefix="plant_care_test_"))
            test_image_loading(test_dir)
    elif args.test_type == "analysis":
        if args.output_dir and os.path.exists(args.output_dir):
            test_image_analysis(args.output_dir)
        else:
            test_dir = create_test_images(args.output_dir or tempfile.mkdtemp(prefix="plant_care_test_"))
            test_image_analysis(test_dir)

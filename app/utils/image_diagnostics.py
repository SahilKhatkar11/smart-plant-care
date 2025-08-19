"""Image diagnostic utilities for troubleshooting image loading issues."""

import os
import io
import sys
import tempfile
from typing import Union, Dict, Any, Optional, BinaryIO, List
import base64
import imghdr
import struct
import binascii
import numpy as np
import streamlit as st
from PIL import Image, ImageFile, UnidentifiedImageError, ExifTags

# Allow loading truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

def diagnose_image(image_data: Union[str, bytes, BinaryIO, Image.Image]) -> Dict[str, Any]:
    """
    Perform comprehensive diagnostics on an image file to identify potential issues.

    Args:
        image_data: Can be a file path, bytes object, file-like object, or PIL Image

    Returns:
        Dict containing diagnostic information and potential issues
    """
    results = {
        "format": None,
        "size_bytes": None,
        "dimensions": None,
        "mode": None,
        "headers": None,
        "magic_bytes": None,
        "issues": [],
        "suggestions": [],
        "valid": False,
        "diagnostics_passed": {},
        "loaded_image": None
    }

    try:
        # Convert to appropriate format for testing
        image_bytes, image_path = _prepare_image_for_diagnosis(image_data)

        if not image_bytes:
            results["issues"].append("Could not read image data")
            results["suggestions"].append("Make sure the file exists and is readable")
            return results

        # Get basic info
        results["size_bytes"] = len(image_bytes)
        if results["size_bytes"] == 0:
            results["issues"].append("Image file is empty (0 bytes)")
            results["suggestions"].append("Check if file was corrupted during transfer or is a placeholder")
            return results

        # Check magic bytes
        results["magic_bytes"] = binascii.hexlify(image_bytes[:16]).decode('ascii')
        results["format"] = _identify_format_from_magic_bytes(image_bytes)

        # Check header structure
        header_issues = _check_image_header(image_bytes, results["format"])
        if header_issues:
            results["issues"].extend(header_issues)
            results["headers"] = "Invalid"
        else:
            results["headers"] = "Valid"

        # Try multiple loading methods
        image, method_results = _try_multiple_loading_methods(image_data)
        results["diagnostics_passed"] = method_results

        if image is not None:
            results["valid"] = True
            results["loaded_image"] = image
            results["dimensions"] = (image.width, image.height)
            results["mode"] = image.mode

            # Check for problematic dimensions
            if image.width <= 0 or image.height <= 0:
                results["valid"] = False
                results["issues"].append(f"Invalid image dimensions: {results['dimensions']}")
                results["suggestions"].append("Image has invalid dimensions, please check the file")

            # Check for unusual image modes
            if image.mode not in ['RGB', 'RGBA', 'L', 'P']:
                results["issues"].append(f"Unusual image mode: {image.mode}")
                results["suggestions"].append("Try converting to a standard RGB mode")

            # Check for exif orientation
            try:
                exif = image.getexif()
                if exif and ExifTags.Base.Orientation in exif:
                    results["exif_orientation"] = exif[ExifTags.Base.Orientation]
                    if results["exif_orientation"] != 1:
                        results["issues"].append(f"Image has non-standard orientation in EXIF data")
                        results["suggestions"].append("Consider removing EXIF data or fixing orientation")
            except Exception:
                pass
        else:
            # Could not load the image
            results["issues"].append("Failed to load image with any method")
            results["suggestions"].append("The image appears to be corrupted or in an unsupported format")

            # Add more detailed suggestions based on format
            if results["format"]:
                results["suggestions"].append(f"Try converting from {results['format']} to a standard JPG or PNG format")

            # Suggest potential fixes based on the file size
            if results["size_bytes"] > 10 * 1024 * 1024:  # 10MB
                results["suggestions"].append("The file is large (>10MB). Try reducing its size before uploading")

        # Generate summary
        if not results["issues"]:
            results["summary"] = "Image appears to be valid"
        else:
            results["summary"] = f"Found {len(results['issues'])} issues with the image"

        return results

    except Exception as e:
        results["issues"].append(f"Error during diagnosis: {str(e)}")
        results["suggestions"].append("The image appears to be severely corrupted or in an unsupported format")
        return results

def get_sample_healthy_image() -> Image.Image:
    """
    Returns a sample healthy plant image for testing.

    Returns:
        PIL Image of a healthy plant
    """
    # Create a simple green leaf image
    img = Image.new('RGB', (224, 224), color=(0, 100, 0))

    # Add some lighter green areas to simulate healthy leaf pattern
    for i in range(10):
        x = np.random.randint(0, 224)
        y = np.random.randint(0, 224)
        radius = np.random.randint(10, 40)

        for dx in range(-radius, radius):
            for dy in range(-radius, radius):
                if dx*dx + dy*dy < radius*radius:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 224 and 0 <= ny < 224:
                        img.putpixel((nx, ny), (np.random.randint(100, 150), np.random.randint(150, 200), 0))

    return img

def get_sample_unhealthy_image() -> Image.Image:
    """
    Returns a sample unhealthy plant image for testing.

    Returns:
        PIL Image of an unhealthy plant
    """
    # Create a base green leaf image
    img = Image.new('RGB', (224, 224), color=(0, 100, 0))

    # Add brown/yellow spots to simulate disease
    for i in range(20):
        x = np.random.randint(0, 224)
        y = np.random.randint(0, 224)
        radius = np.random.randint(5, 25)

        for dx in range(-radius, radius):
            for dy in range(-radius, radius):
                if dx*dx + dy*dy < radius*radius:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 224 and 0 <= ny < 224:
                        # Brown/yellow spots
                        img.putpixel((nx, ny), (np.random.randint(150, 200), np.random.randint(100, 150), 0))

    return img

def run_image_diagnostic_test(uploaded_file=None):
    """
    Streamlit function to run image diagnostics and display results.

    Args:
        uploaded_file: Optional Streamlit uploaded file
    """
    st.subheader("🔍 Image Diagnostic Tool")

    if uploaded_file is None:
        uploaded_file = st.file_uploader("Upload an image for diagnostics", type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'])

    if uploaded_file:
        with st.spinner("Running image diagnostics..."):
            # Reset file pointer
            uploaded_file.seek(0)

            # Run diagnostics
            results = diagnose_image(uploaded_file)

            # Display results
            st.subheader("Diagnostic Results")

            # Show image if valid
            if results["loaded_image"]:
                st.image(results["loaded_image"], caption="Successfully loaded image", width=300)

            # Basic info
            st.markdown("### Basic Information")
            info_cols = st.columns(2)
            with info_cols[0]:
                st.markdown(f"**Format:** {results['format'] or 'Unknown'}")
                st.markdown(f"**Size:** {_format_size(results['size_bytes'])}")
                if results["dimensions"]:
                    st.markdown(f"**Dimensions:** {results['dimensions'][0]} x {results['dimensions'][1]} pixels")
                else:
                    st.markdown("**Dimensions:** Unknown")

            with info_cols[1]:
                st.markdown(f"**Color Mode:** {results['mode'] or 'Unknown'}")
                st.markdown(f"**Headers:** {results['headers'] or 'Unknown'}")
                st.markdown(f"**Status:** {'✅ Valid' if results['valid'] else '❌ Invalid'}")

            # Magic bytes
            if results["magic_bytes"]:
                with st.expander("Technical Details"):
                    st.markdown(f"**Magic Bytes (hex):** `{results['magic_bytes']}`")

                    # Show loading method results
                    st.markdown("### Loading Method Results")
                    for method, passed in results["diagnostics_passed"].items():
                        st.markdown(f"- {method}: {'✅ Passed' if passed else '❌ Failed'}")

            # Issues
            if results["issues"]:
                st.markdown("### Issues Detected")
                for issue in results["issues"]:
                    st.markdown(f"- ❌ {issue}")

            # Suggestions
            if results["suggestions"]:
                st.markdown("### Suggestions")
                for suggestion in results["suggestions"]:
                    st.markdown(f"- 💡 {suggestion}")

            # Show sample images if needed
            if not results["valid"]:
                st.markdown("### Sample Images")
                st.markdown("If you're having trouble with your image, you can try one of these sample images:")

                sample_cols = st.columns(2)
                with sample_cols[0]:
                    healthy_img = get_sample_healthy_image()
                    st.image(healthy_img, caption="Sample Healthy Plant", width=200)
                    if st.button("Use Healthy Sample"):
                        return healthy_img

                with sample_cols[1]:
                    unhealthy_img = get_sample_unhealthy_image()
                    st.image(unhealthy_img, caption="Sample Unhealthy Plant", width=200)
                    if st.button("Use Unhealthy Sample"):
                        return unhealthy_img
    else:
        st.info("Upload an image to run diagnostics")

    return None

def repair_image(image_data: Union[str, bytes, BinaryIO, Image.Image]) -> Optional[Image.Image]:
    """
    Attempt to repair a problematic image by reprocessing it.

    Args:
        image_data: Image data to repair

    Returns:
        Repaired PIL Image or None if repair failed
    """
    try:
        image_bytes, _ = _prepare_image_for_diagnosis(image_data)
        if not image_bytes:
            return None

        # Method 1: Reprocess through BytesIO
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.load()  # Force load

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize slightly to trigger reprocessing
            img = img.resize((img.width, img.height))

            # Test validity
            test_array = np.array(img)
            if test_array.size == 0:
                raise ValueError("Empty image array")

            return img
        except Exception:
            pass

        # Method 2: Try reencoding as PNG
        try:
            # Write to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_file.write(image_bytes)
                tmp_file.flush()

                img = Image.open(tmp_file.name)
                img.load()

                # Save to new BytesIO with explicit format
                output = io.BytesIO()
                img.save(output, format='PNG')
                output.seek(0)

                # Reload from the newly saved bytes
                repaired = Image.open(output)
                repaired.load()

                # Clean up temp file
                os.unlink(tmp_file.name)

                return repaired
        except Exception:
            # Clean up temp file in case of exception
            if 'tmp_file' in locals():
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass

        # Method 3: Try via numpy array if possible
        try:
            import cv2
            # Try to get numpy array
            if isinstance(image_data, np.ndarray):
                array = image_data
            elif isinstance(image_data, Image.Image):
                array = np.array(image_data)
            else:
                # Save to temp file and use OpenCV
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                    tmp_file.write(image_bytes)
                    tmp_file.flush()

                    array = cv2.imread(tmp_file.name)
                    os.unlink(tmp_file.name)

                    if array is None:
                        return None

                    # Convert BGR to RGB
                    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)

            # Create a new PIL image from the array
            return Image.fromarray(array)
        except Exception:
            pass

        return None
    except Exception:
        return None

def _prepare_image_for_diagnosis(image_data: Union[str, bytes, BinaryIO, Image.Image]) -> tuple:
    """Prepare image data for diagnosis by converting to bytes and optionally path."""
    image_bytes = None
    image_path = None

    # Convert to bytes based on input type
    if isinstance(image_data, str):
        # It's a file path
        image_path = image_data
        with open(image_data, 'rb') as f:
            image_bytes = f.read()

    elif isinstance(image_data, bytes):
        # Already bytes
        image_bytes = image_data

    elif isinstance(image_data, Image.Image):
        # PIL Image, convert to bytes
        buffer = io.BytesIO()
        image_data.save(buffer, format=image_data.format or 'PNG')
        image_bytes = buffer.getvalue()

    elif hasattr(image_data, 'read'):
        # File-like object
        if hasattr(image_data, 'seek'):
            image_data.seek(0)
        image_bytes = image_data.read()
        if hasattr(image_data, 'seek'):
            image_data.seek(0)

        # If it has a name attribute, it might be a file path
        if hasattr(image_data, 'name'):
            image_path = getattr(image_data, 'name')

    return image_bytes, image_path

def _identify_format_from_magic_bytes(image_bytes: bytes) -> Optional[str]:
    """Identify image format from magic bytes."""
    # Some common image format signatures
    signatures = {
        b'\xff\xd8\xff': 'JPEG',
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'GIF87a': 'GIF',
        b'GIF89a': 'GIF',
        b'BM': 'BMP',
        b'II*\x00': 'TIFF',
        b'MM\x00*': 'TIFF',
        b'RIFF': 'WEBP',  # WEBP starts with RIFF
        # Add more signatures as needed
    }

    for signature, format_name in signatures.items():
        if image_bytes.startswith(signature):
            return format_name

    # Try imghdr as a fallback
    format_imghdr = imghdr.what(None, h=image_bytes)
    if format_imghdr:
        return format_imghdr.upper()

    return None

def _check_image_header(image_bytes: bytes, format_name: Optional[str]) -> List[str]:
    """Check if image header is valid for the identified format."""
    issues = []

    if not format_name:
        issues.append("Could not identify image format from header")
        return issues

    # Check format-specific headers
    if format_name == 'JPEG':
        # JPEG should start with SOI marker (0xFFD8) and end with EOI marker (0xFFD9)
        if not image_bytes.startswith(b'\xff\xd8'):
            issues.append("Invalid JPEG header: missing SOI marker")
        if not image_bytes.endswith(b'\xff\xd9'):
            issues.append("Invalid JPEG trailer: missing EOI marker")

    elif format_name == 'PNG':
        # PNG should have IHDR chunk after signature
        if len(image_bytes) >= 24:  # Signature (8) + Chunk length (4) + "IHDR" (4) + Width (4) + Height (4)
            try:
                chunk_length = struct.unpack('>I', image_bytes[8:12])[0]
                chunk_type = image_bytes[12:16]
                if chunk_type != b'IHDR':
                    issues.append("Invalid PNG structure: first chunk is not IHDR")

                # Check width and height
                width = struct.unpack('>I', image_bytes[16:20])[0]
                height = struct.unpack('>I', image_bytes[20:24])[0]
                if width == 0 or height == 0:
                    issues.append(f"Invalid PNG dimensions: {width}x{height}")
            except Exception:
                issues.append("Could not parse PNG chunk structure")
        else:
            issues.append("PNG file too small to contain valid header")

    # Add more format-specific checks as needed

    return issues

def _try_multiple_loading_methods(image_data: Union[str, bytes, BinaryIO, Image.Image]) -> tuple:
    """Try multiple methods to load an image and return success results."""
    results = {
        "PIL direct": False,
        "PIL via file": False,
        "OpenCV": False,
        "Pillow with different modes": False
    }

    # Method 1: Direct PIL
    try:
        if isinstance(image_data, str):
            image = Image.open(image_data)
        elif isinstance(image_data, Image.Image):
            image = image_data.copy()
        elif isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        else:
            # File-like object
            if hasattr(image_data, 'seek'):
                image_data.seek(0)
            image = Image.open(image_data)
            if hasattr(image_data, 'seek'):
                image_data.seek(0)

        image.load()  # Force load
        results["PIL direct"] = True
        return image, results
    except Exception:
        pass

    # Method 2: PIL via temporary file
    try:
        image_bytes, _ = _prepare_image_for_diagnosis(image_data)
        if image_bytes:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_file.write(image_bytes)
                tmp_file.flush()

                image = Image.open(tmp_file.name)
                image.load()

                # Clean up
                os.unlink(tmp_file.name)

                results["PIL via file"] = True
                return image, results
    except Exception:
        # Clean up temp file in case of exception
        if 'tmp_file' in locals():
            try:
                os.unlink(tmp_file.name)
            except:
                pass

    # Method 3: OpenCV
    try:
        import cv2
        image_bytes, image_path = _prepare_image_for_diagnosis(image_data)

        if image_path and os.path.exists(image_path):
            # Direct file path
            cv_img = cv2.imread(image_path)
            if cv_img is not None and cv_img.size > 0:
                # Convert BGR to RGB
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(cv_img)
                results["OpenCV"] = True
                return image, results

        if image_bytes:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_file.write(image_bytes)
                tmp_file.flush()

                cv_img = cv2.imread(tmp_file.name)
                os.unlink(tmp_file.name)

                if cv_img is not None and cv_img.size > 0:
                    # Convert BGR to RGB
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(cv_img)
                    results["OpenCV"] = True
                    return image, results
    except Exception:
        pass

    # Method 4: Try different PIL modes
    try:
        image_bytes, _ = _prepare_image_for_diagnosis(image_data)
        if image_bytes:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_file.write(image_bytes)
                tmp_file.flush()

                for mode in ['RGB', 'RGBA', 'L', 'P', '1']:
                    try:
                        image = Image.open(tmp_file.name)
                        image.load()
                        image = image.convert(mode)

                        # Clean up
                        os.unlink(tmp_file.name)

                        results["Pillow with different modes"] = True
                        return image, results
                    except Exception:
                        continue

                # Clean up if all modes failed
                os.unlink(tmp_file.name)
    except Exception:
        # Clean up temp file in case of exception
        if 'tmp_file' in locals():
            try:
                os.unlink(tmp_file.name)
            except:
                pass

    # All methods failed
    return None, results

def _format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

if __name__ == "__main__":
    # This script can be run directly for command-line diagnostics
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if os.path.exists(image_path):
            results = diagnose_image(image_path)
            print(f"Image Diagnostics for: {image_path}")
            print(f"Format: {results['format'] or 'Unknown'}")
            print(f"Size: {_format_size(results['size_bytes'])}")
            if results['dimensions']:
                print(f"Dimensions: {results['dimensions'][0]} x {results['dimensions'][1]} pixels")
            print(f"Valid: {'Yes' if results['valid'] else 'No'}")

            if results['issues']:
                print("\nIssues:")
                for issue in results['issues']:
                    print(f"- {issue}")

            if results['suggestions']:
                print("\nSuggestions:")
                for suggestion in results['suggestions']:
                    print(f"- {suggestion}")
        else:
            print(f"Error: File not found: {image_path}")
    else:
        print("Usage: python image_diagnostics.py <image_path>")

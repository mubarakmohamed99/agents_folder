"""Odoo download and extraction utilities."""

import os
from typing import Optional, Tuple

import requests
import zipfile
import tarfile


def download_odoo(
    version: str = "16.0",
    target_dir: str = ".",
    download_url: Optional[str] = None,
) -> Tuple[bool, str]:
    """Download and extract the specified Odoo version.

    Args:
        version: Odoo version to download (for example, "16.0").
        target_dir: Directory where archives and extracted files are stored.
        download_url: Optional direct URL to the Odoo archive. If omitted, a
            GitHub branch zip URL for the given version is used.

    Returns:
        Tuple[bool, str]: (success_flag, path_to_extracted_odoo_source or "").
    """

    print(f"Downloading Odoo version {version} to {target_dir}...")

    if download_url is None:
        download_url = f"https://github.com/odoo/odoo/archive/refs/heads/{version}.zip"
        print(f"No download URL provided. Using default: {download_url}")

    os.makedirs(target_dir, exist_ok=True)

    # Determine archive filename based on URL extension.
    filename = os.path.join(target_dir, f"odoo_{version}.zip")
    if download_url.endswith(".tar.gz"):
        filename = os.path.join(target_dir, f"odoo_{version}.tar.gz")
    elif download_url.endswith(".zip"):
        filename = os.path.join(target_dir, f"odoo_{version}.zip")

    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded {download_url} to {filename}")

        extract_path = os.path.join(target_dir, f"odoo_{version}_extracted")
        os.makedirs(extract_path, exist_ok=True)

        if filename.endswith(".zip"):
            with zipfile.ZipFile(filename, "r") as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"Extracted zip archive to {extract_path}")
        elif filename.endswith(".tar.gz"):
            with tarfile.open(filename, "r:gz") as tar_ref:
                tar_ref.extractall(extract_path)
            print(f"Extracted tar.gz archive to {extract_path}")
        else:
            print(
                f"Unsupported archive format: {filename}. Only .zip and .tar.gz "
                "are supported for automatic extraction."
            )
            return False, ""

        # Try to find the actual Odoo source directory inside the extracted
        # folder (GitHub archives usually add a top-level directory).
        extracted_dirs = [
            d
            for d in os.listdir(extract_path)
            if os.path.isdir(os.path.join(extract_path, d))
        ]
        if extracted_dirs:
            odoo_source_path = os.path.join(extract_path, extracted_dirs[0])
            print(f"Identified Odoo source path: {odoo_source_path}")
            return True, odoo_source_path

        print(
            f"Warning: No subdirectory found in {extract_path}. Assuming Odoo "
            "source is directly in the extraction directory."
        )
        return True, extract_path

    except requests.exceptions.RequestException as exc:
        print(f"Error during download: {exc}")
        return False, ""
    except (zipfile.BadZipFile, tarfile.ReadError) as exc:
        print(f"Error extracting archive: {exc}")
        return False, ""
    except Exception as exc:  # pragma: no cover - generic safety net
        print(f"An unexpected error occurred: {exc}")
        return False, ""

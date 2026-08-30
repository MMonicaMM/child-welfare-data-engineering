from pathlib import Path
from datetime import datetime, timezone
import hashlib

import requests
import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "rzs"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SOURCE_URL = SOURCE_URL = (
    "https://data.gov.rs/s/resources/"
    "statistichki-godishnjak-2019-sotsijalna-zashtita/"
    "20210725-002935/"
    "detsa-i-omladina-korisnitsi-sotsijalne-zashtite.xlsx"
)

OUTPUT_FILE = RAW_DIR / "children_social_protection.xlsx"


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 checksum of a downloaded file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def download_file(url: str, output_path: Path) -> None:
    """Download a file from a public URL."""

    print(f"Downloading: {url}")

    response = requests.get(
        url,
        timeout=60,
        headers={
            "User-Agent": "child-welfare-data-engineering/1.0"
        },
    )

    response.raise_for_status()

    with open(output_path, "wb") as file:
        file.write(response.content)

    print(f"Saved to: {output_path}")


def inspect_excel(file_path: Path) -> None:
    """Inspect downloaded Excel file."""

    print("\nReading Excel file...")

    excel_file = pd.ExcelFile(file_path)

    print("\nAvailable sheets:")
    for sheet in excel_file.sheet_names:
        print(f" - {sheet}")

    first_sheet = excel_file.sheet_names[0]

    df = pd.read_excel(
        file_path,
        sheet_name=first_sheet
    )

    print(f"\nSelected sheet: {first_sheet}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f" - {column}")

    print("\nFirst 5 rows:")
    print(df.head())


def create_metadata(file_path: Path) -> None:
    """Create metadata file for the raw dataset."""

    checksum = calculate_sha256(file_path)

    metadata_file = file_path.with_suffix(".metadata.txt")

    downloaded_at = datetime.now(timezone.utc).isoformat()

    metadata = f"""Source URL:
{SOURCE_URL}

Downloaded at:
{downloaded_at}

File:
{file_path.name}

SHA-256:
{checksum}
"""

    metadata_file.write_text(
        metadata,
        encoding="utf-8"
    )

    print(f"\nMetadata saved to: {metadata_file}")


# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def main():

    if SOURCE_URL == "PASTE_RZS_RESOURCE_URL_HERE":
        raise ValueError(
            "Please provide the exact RZS resource URL "
            "in SOURCE_URL before running the script."
        )

    download_file(
        SOURCE_URL,
        OUTPUT_FILE
    )

    create_metadata(
        OUTPUT_FILE
    )

    inspect_excel(
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()
from pathlib import Path
from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError
import time


SOURCE_FOLDER = Path(r"E:\data")
BUCKET_NAME = "olist-analysis-bucket"
DESTINATION_FOLDER = "historical_data"


def upload_files():

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    csv_files = list(SOURCE_FOLDER.glob("*.csv"))

    print(f"Found {len(csv_files)} CSV files.\n")

    uploaded = 0
    skipped = 0
    failed = 0

    for file in csv_files:

        destination = f"{DESTINATION_FOLDER}/{file.name}"
        blob = bucket.blob(destination)

        # Skip files that are already in GCS
        if blob.exists():
            print(f"Skipping {file.name} - already exists")
            skipped += 1
            continue

        print(f"Uploading {file.name}...")

        for attempt in range(1, 4):

            try:
                blob.upload_from_filename(
                    str(file),
                    content_type="text/csv",
                    timeout=300
                )

                print(f"Uploaded {file.name}\n")
                uploaded += 1
                break

            except Exception as error:

                print(
                    f"Attempt {attempt} failed for {file.name}: {error}"
                )

                if attempt < 3:
                    print("Retrying...\n")
                    time.sleep(5)
                else:
                    print(f"Failed to upload {file.name}\n")
                    failed += 1

    print("=" * 50)
    print("UPLOAD SUMMARY")
    print("=" * 50)

    print(f"Total files : {len(csv_files)}")
    print(f"Uploaded    : {uploaded}")
    print(f"Skipped     : {skipped}")
    print(f"Failed      : {failed}")


if __name__ == "__main__":
    upload_files()
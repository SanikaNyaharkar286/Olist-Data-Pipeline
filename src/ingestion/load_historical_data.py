"""
Upload cleaned CSVs to GCS. Always overwrites — no skip-if-exists,
because that would silently block a fix from landing on a re-run
(a broken file already in the bucket would just get skipped forever).
"""
 
from pathlib import Path
from google.cloud import storage
 
BUCKET_NAME = "olist-analysis-bucket"
GCS_FOLDER = "historical_data"
 
 
def upload_files(files: list[Path]) -> list[Path]:
    print("\n" + "=" * 60)
    print("STEP 2: UPLOAD TO GCS")
    print("=" * 60)
 
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
 
    uploaded = []
 
    for file in files:
        destination = f"{GCS_FOLDER}/{file.name}"
        blob = bucket.blob(destination)
 
        try:
            blob.upload_from_filename(str(file), content_type="text/csv", timeout=300)
            print(f"   ✅ Uploaded {file.name} -> gs://{BUCKET_NAME}/{destination}")
            uploaded.append(file)
        except Exception as e:
            print(f"   ❌ Failed to upload {file.name}: {e}")
 
    print(f"\n✅ {len(uploaded)}/{len(files)} files uploaded")
    return uploaded
 
 
if __name__ == "__main__":
    print("Run the pipeline from main.py")
"""
Load uploaded CSVs from GCS into BigQuery Bronze tables.
 
allow_quoted_newlines=True is required here regardless of how clean the
quoting is, because text fields (e.g. review comments) can contain real
line breaks inside a quoted field.
"""
 
from pathlib import Path
from google.cloud import bigquery
 
BQ_PROJECT = "rare-bastion-503107-q3"     # <-- set this
BQ_DATASET = "olist_bronze_layer"          # <-- set this
 
BUCKET_NAME = "olist-analysis-bucket"
GCS_FOLDER = "historical_data"
 
 
def load_to_bigquery(files: list[Path]):
    print("\n" + "=" * 60)
    print("STEP 3: LOAD INTO BIGQUERY")
    print("=" * 60)
 
    client = bigquery.Client(project=BQ_PROJECT)
 
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",  # replace bronze table each run
    )
 
    loaded, failed = 0, 0
 
    for file in files:
        table_name = file.stem
        table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{table_name}"
        gcs_uri = f"gs://{BUCKET_NAME}/{GCS_FOLDER}/{file.name}"
 
        print(f"\n   Loading {table_name} from {gcs_uri}...")
 
        try:
            job = client.load_table_from_uri(gcs_uri, table_id, job_config=job_config)
            job.result()
            table = client.get_table(table_id)
            print(f"   ✅ Loaded {table.num_rows} rows into {table_id}")
            loaded += 1
        except Exception as e:
            print(f"   ❌ Failed to load {table_name}: {e}")
            failed += 1
 
    print(f"\n✅ {loaded} tables loaded, ❌ {failed} failed")
 
 
if __name__ == "__main__":
    print("Run the pipeline from main.py")
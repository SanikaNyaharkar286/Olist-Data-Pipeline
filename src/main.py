from validation.validator import validate_and_clean_files
from ingestion.load_historical_data import upload_files
from transform.bronze.load_bronze import load_to_bigquery

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
 
def main():
    print("STARTING PIPELINE", flush=True)
    print("=" * 60)
    print("OLIST DATA PIPELINE")
    print("=" * 60)
 
    cleaned_files = validate_and_clean_files()
    if not cleaned_files:
        print("\nNo valid files to process. Stopping.")
        return
 
    uploaded_files = upload_files(cleaned_files)
    if not uploaded_files:
        print("\nNo files uploaded. Stopping.")
        return
 
    load_to_bigquery(uploaded_files)
 
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
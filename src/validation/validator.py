"""
Validation + cleaning.
 
Instead of hand-patching quote characters line-by-line (unsafe — text
fields like review comments contain embedded newlines and stray quotes
that break that approach), we let pandas parse the file once and rewrite
it. pandas' default CSV writer applies correct RFC 4180 quoting, which is
exactly what fixes BigQuery's "Missing close quote character" error.
"""
 
from pathlib import Path
import pandas as pd
 
SOURCE_FOLDER = Path(r"E:\data")
CLEANED_FOLDER = SOURCE_FOLDER / "cleaned"
 
 
def clean_csv(file_path: Path):
    print(f"\nProcessing: {file_path.name}")
 
    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    except Exception as e1:
        print(f"   Default parser failed ({e1}); retrying with python engine...")
        try:
            df = pd.read_csv(
                file_path,
                encoding="utf-8-sig",
                engine="python",
                on_bad_lines="warn",
            )
        except Exception as e2:
            print(f"   ❌ Could not read file: {e2}")
            return None
 
    if df.empty:
        print("   ❌ File has no rows")
        return None
 
    print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
 
    CLEANED_FOLDER.mkdir(parents=True, exist_ok=True)
    cleaned_path = CLEANED_FOLDER / file_path.name  # same filename, new folder
 
    df.to_csv(cleaned_path, index=False, encoding="utf-8")
 
    print(f"   ✅ Cleaned -> {cleaned_path}")
    return cleaned_path
 
 
def validate_and_clean_files():
    print("=" * 60)
    print("STEP 1: VALIDATE + CLEAN")
    print("=" * 60)
 
    csv_files = sorted(SOURCE_FOLDER.glob("*.csv"))
    cleaned_files = []
 
    for f in csv_files:
        result = clean_csv(f)
        if result is not None:
            cleaned_files.append(result)
 
    print(f"\n✅ {len(cleaned_files)}/{len(csv_files)} files cleaned and ready")
    return cleaned_files
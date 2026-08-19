module "bucket" {
  source  = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version = "~> 12.3"

  name       = "olist-analysis-bucket"
  project_id = "rare-bastion-503107-q3"
  location   = "us-east1"

  iam_members = [{
    role   = "roles/storage.objectViewer"
    member = "serviceAccount:rukmini-terraform-service-acc@rare-bastion-503107-q3.iam.gserviceaccount.com"
  }]
}

resource "google_storage_bucket_object" "historical_data" {
  name    = "historical_data/"
  bucket  = module.bucket.name
  content = " "
}

resource "google_storage_bucket_object" "delta" {
  name    = "delta/"
  bucket  = module.bucket.name
  content = " "
}
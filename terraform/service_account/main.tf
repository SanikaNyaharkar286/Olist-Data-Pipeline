resource "google_service_account" "service_account" {
  account_id   = var.service_account_id
  display_name = var.display_name
  description  = "Created using Terraform"
}

locals {
  sa_roles = [
    "roles/storage.objectAdmin",
    "roles/bigquery.jobUser",
    "roles/bigquery.dataEditor",
    "roles/bigquery.dataViewer"
  ]
}

resource "google_project_iam_member" "sa_roles" {
  for_each = toset(local.sa_roles)

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.service_account.email}"
}
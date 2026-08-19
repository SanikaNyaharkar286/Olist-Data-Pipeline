resource "google_bigquery_dataset" "datasets" {
  for_each = var.datasets

  dataset_id    = each.key
  project       = var.project_id
  friendly_name = each.value.friendly_name
  description   = each.value.description
  location      = var.dataset_location
  labels        = each.value.labels

  delete_contents_on_destroy = false
}
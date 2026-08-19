output "dataset_ids" {
  description = "IDs of the created BigQuery datasets"
  value       = { for k, v in google_bigquery_dataset.datasets : k => v.dataset_id }
}

output "dataset_self_links" {
  description = "Self links of the created BigQuery datasets"
  value       = { for k, v in google_bigquery_dataset.datasets : k => v.self_link }
}
output "bucket_name" {
  value = module.bucket.name
}

output "bucket_url" {
  value = "gs://${var.bucket_name}"
}
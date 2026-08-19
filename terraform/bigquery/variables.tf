variable "project_id" {
  type        = string
  description = "rare-bastion-503107-q3"
}

variable "region" {
  type        = string
  description = "Default region for the provider"
  default     = "us-east1"
}

variable "dataset_location" {
  type        = string
  description = "Location for the BigQuery datasets (e.g. US, EU, us-east1)"
  default     = "us-east1"
}

variable "datasets" {
  type = map(object({
    friendly_name = string
    description   = string
    labels        = optional(map(string), {})
  }))
  description = "Map of BigQuery datasets to create"
}

# * STACK_VARS* #

variable "stack_name" {
  type        = string
  description = "The default namespace to use in all service name. This is used to easyly identify the resources of the project"
  default     = "YurbDev"
}

variable "stack_environment" {
  type    = string
  default = "production"
}

# * MAIN_VARS * #

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "cloudflare_api_token" {
  type      = string
  sensitive = true
}

# * ROUTE53_VARS * #

variable "domains" {
  type = object({
    main_fqdn = string
    cdn_fqdn  = string
    api_fqdn  = string
  })
}

variable "frontend_records" {
  type = object({
    main_fqdn = string
    www       = string
  })
}

# * CDN_VARS * #

variable "cdn_bucket_name" {
  type      = string
  sensitive = true
}

variable "cnd_origin_path" {
  type    = string
  default = "/assets"
}

# * RDS_VARS * #

variable "rds_identifier" {
  type      = string
  sensitive = true
}

variable "rds_username" {
  type      = string
  sensitive = true
}

variable "rds_password" {
  type      = string
  sensitive = true
}

variable "rds_db_name" {
  type      = string
  sensitive = true
}

# * CLUSTER_VARS * #

variable "lt_instance_type" {
  type    = string
  default = "t2.micro"
}

variable "lt_ebs_volume_size" {
  type    = number
  default = 30
}

# * SERVICE_VARS * #

variable "force_deploy" {
  type        = bool
  default     = false
  description = "If true, force the service to redeploy"
}

# * TASK_DEFINITION_VARS * #

variable "td_docker_image" {
  type      = string
  sensitive = true
}

variable "td_container_name" {
  type    = string
  default = "backend-service"
}

variable "td_container_port" {
  type = number
}
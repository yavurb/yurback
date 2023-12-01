terraform {
  required_version = ">= 1.6.3, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.24.0, < 6.0.0"
    }

    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = ">= 4.20.0, < 5.0.0"
    }
  }

  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

locals {
  stack_env_title = title(var.stack_environment)
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

data "aws_subnets" "default_subnets" {
  filter {
    name   = "vpc-id"
    values = [aws_default_vpc.default.id]
  }
}

data "cloudflare_zone" "main_domain" {
  name = var.domains.main_fqdn
}

resource "aws_acm_certificate" "main_domain" {
  domain_name               = var.domains.main_fqdn
  subject_alternative_names = [var.domains.cdn_fqdn, var.domains.api_fqdn]
  validation_method         = "DNS"

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}


resource "cloudflare_record" "main_records" {
  for_each = {
    for dvo in aws_acm_certificate.main_domain.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      record  = dvo.resource_record_value
      type    = dvo.resource_record_type
      zone_id = data.cloudflare_zone.main_domain.id
    }
  }

  allow_overwrite = true
  name            = each.value.name
  value           = each.value.record
  ttl             = 60
  type            = each.value.type
  zone_id         = each.value.zone_id
}

resource "aws_acm_certificate_validation" "validate_records" {
  depends_on = [cloudflare_record.main_records]

  certificate_arn         = aws_acm_certificate.main_domain.arn
  validation_record_fqdns = [for record in cloudflare_record.main_records : record.hostname]
}

# --- Frontend Resources ---- #

resource "cloudflare_record" "main_frontend_records" {
  for_each = {
    yurb = {
      name   = var.domains.main_fqdn
      type   = "A"
      record = var.frontend_records.main_fqdn
    }
    www = {
      name   = "www"
      type   = "CNAME"
      record = var.frontend_records.www
    }
  }

  zone_id = data.cloudflare_zone.main_domain.id
  name    = each.value.name
  type    = each.value.type
  value   = each.value.record
  ttl     = 300
}
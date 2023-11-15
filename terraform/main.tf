terraform {
  required_version = ">= 1.6.3, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.24.0, < 6.0.0"
    }

    namecheap = {
      source  = "namecheap/namecheap"
      version = ">= 2.1.0, < 3.0.0"
    }
  }

  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

provider "namecheap" {
  user_name = var.namecheap_credentials.user
  api_user  = var.namecheap_credentials.api_user
  api_key   = var.namecheap_credentials.api_key
}

resource "aws_acm_certificate" "yurb" {
  domain_name               = var.domains.main_fqdn
  subject_alternative_names = [var.domains.cdn_fqdn, var.domains.api_fqdn]
  validation_method         = "DNS"

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}

resource "aws_route53_zone" "yurb_dev" {
  name = var.domains.main_fqdn

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}

resource "aws_route53_record" "yurb" {
  for_each = {
    for dvo in aws_acm_certificate.yurb.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      record  = dvo.resource_record_value
      type    = dvo.resource_record_type
      zone_id = aws_route53_zone.yurb_dev.zone_id
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = each.value.zone_id
}

resource "aws_acm_certificate_validation" "validate_records" {
  certificate_arn         = aws_acm_certificate.yurb.arn
  validation_record_fqdns = [for record in aws_route53_record.yurb : record.fqdn]
}

resource "namecheap_domain_records" "yurb_dev" {
  domain      = var.domains.main_fqdn
  mode        = "OVERWRITE"
  nameservers = aws_route53_zone.yurb_dev.name_servers
}

# --- Frontend Resources ---- #

resource "aws_route53_record" "yurb_dev" {
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

  zone_id = aws_route53_zone.yurb_dev.zone_id
  name    = each.value.name
  type    = each.value.type
  records = [each.value.record]
  ttl     = 300
}
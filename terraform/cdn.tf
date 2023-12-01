resource "aws_s3_bucket" "app_bucket" {
  bucket = var.cdn_bucket_name

  tags = {
    Name        = "${var.stack_name} ${local.stack_env_title}"
    environment = var.stack_environment
    project     = var.stack_name
  }
}

data "aws_cloudfront_cache_policy" "cdn_managed_cp" {
  name = "Managed-CachingOptimized"
}

resource "aws_cloudfront_origin_access_control" "cdn_s3_oac" {
  name                              = "${var.stack_name}-s3-OriginAccessControl"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "cdn" {
  # This helps the distribution to wait until all the ssl/tls certs are validated to avoid errors when assigning the viewer certificate
  depends_on = [aws_acm_certificate_validation.validate_records]

  origin {
    domain_name              = aws_s3_bucket.app_bucket.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.cdn_s3_oac.id
    origin_id                = aws_s3_bucket.app_bucket.id
    origin_path              = var.cnd_origin_path
  }

  enabled = true
  aliases = [var.domains.cdn_fqdn]

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = aws_s3_bucket.app_bucket.id
    cache_policy_id        = data.aws_cloudfront_cache_policy.cdn_managed_cp.id
    viewer_protocol_policy = "redirect-to-https"
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.main_domain.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      locations        = []
      restriction_type = "none"
    }
  }

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}

data "aws_iam_policy_document" "cf_s3_policy" {
  policy_id = "PolicyForCloudFrontPrivateContent"
  statement {
    sid    = "AllowCloudFrontServicePrincipal"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::${var.cdn_bucket_name}/*"]
    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.cdn.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "allow_access_from_cloudfront" {
  bucket = aws_s3_bucket.app_bucket.id
  policy = data.aws_iam_policy_document.cf_s3_policy.json
}

# * Create CDN record * #

resource "cloudflare_record" "cdn" {
  depends_on = [aws_cloudfront_distribution.cdn]

  zone_id = data.cloudflare_zone.main_domain.id
  name    = var.domains.cdn_fqdn
  type    = "CNAME"
  value   = aws_cloudfront_distribution.cdn.domain_name
  ttl = 300
}

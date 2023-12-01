resource "aws_security_group" "allow_alb_http_traffic" {
  name        = "allow_http_https"
  description = "Allow HTTP and HTTPS traffic into the ALB"
  vpc_id      = aws_default_vpc.default.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_http_https"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_http" {
  security_group_id = aws_security_group.allow_alb_http_traffic.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  ip_protocol = "tcp"
  to_port     = 80
}

resource "aws_vpc_security_group_ingress_rule" "allow_https" {
  security_group_id = aws_security_group.allow_alb_http_traffic.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  ip_protocol = "tcp"
  to_port     = 443
}

resource "aws_lb" "app_load_balancer" {
  name               = "${var.stack_name}-LoadBalancer-${local.stack_env_title}"
  internal           = false
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default_subnets.ids

  security_groups = [aws_security_group.allow_alb_http_traffic.id]

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}

resource "aws_lb_target_group" "app_lb_target_group" {
  name     = "${var.stack_name}-LBTargetGroup-${local.stack_env_title}"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_default_vpc.default.id

  health_check {
    healthy_threshold = 2
    path              = "/"
    matcher           = "200-299"
  }

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}

resource "aws_lb_listener" "app_lb_http_listener" {
  load_balancer_arn = aws_lb.app_load_balancer.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_lb_target_group.arn
  }
}

resource "aws_lb_listener" "app_lb_https_listener" {
  depends_on = [aws_acm_certificate.main_domain]

  load_balancer_arn = aws_lb.app_load_balancer.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.main_domain.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_lb_target_group.arn
  }
}

# * Create API record * #

resource "cloudflare_record" "api" {
  depends_on = [aws_lb.app_load_balancer]

  zone_id = data.cloudflare_zone.main_domain.id
  name    = var.domains.api_fqdn
  type    = "CNAME"
  value   = lower(aws_lb.app_load_balancer.dns_name)
  ttl = 300
}

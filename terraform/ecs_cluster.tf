resource "aws_security_group" "allow_components_traffic" {
  name        = "${var.stack_name}_ContainerInstanceSG_${var.stack_environment}"
  description = "Allow inbound traffic from ALB and outbound traffic to RDS Cluster"
  vpc_id      = aws_default_vpc.default.id

  tags = {
    Name = "allow_${var.stack_name}_traffic"
  }
}

resource "aws_default_security_group" "default_security_group" {
  vpc_id = aws_default_vpc.default.id

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_yurb_dev_lb_prod" {
  security_group_id            = aws_security_group.allow_components_traffic.id
  referenced_security_group_id = aws_security_group.allow_alb_http_traffic.id

  from_port   = 0
  to_port     = 65535
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "allow_traffic_to_rds" {
  security_group_id            = aws_security_group.allow_components_traffic.id
  referenced_security_group_id = aws_security_group.allow_app_traffic.id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al202*-ami-ecs-hvm-*-x86_64"]
  }
}

data "aws_iam_policy_document" "trusted_ecs_instance_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com", "ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "ecsInstanceRole"
}

resource "aws_launch_template" "yurb_dev_lt" {
  name                   = "${var.stack_name}_ECSLT"
  instance_type          = var.lt_instance_type
  vpc_security_group_ids = [aws_default_security_group.default_security_group.id, aws_security_group.allow_components_traffic.id]
  image_id               = data.aws_ami.amazon_linux.id
  iam_instance_profile {
    arn = data.aws_iam_instance_profile.ecs_instance_profile.arn
  }

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      volume_size = var.lt_ebs_volume_size
    }
  }

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }

  user_data = base64encode(
    templatefile(
      "${path.module}/user_data.tftpl", { ecs_cluster_name = "${var.stack_name}${title(var.stack_environment)}" }
    )
  )
}

resource "aws_autoscaling_group" "yurb_dev_ecs_asg" {
  name             = "${var.stack_name}_ClusterASG_${var.stack_environment}"
  max_size         = 1
  min_size         = 1
  desired_capacity = 1
  # health_check_type     = "EC2"
  vpc_zone_identifier = data.aws_subnets.default_subnets.ids
  # default_instance_warmup = 180
  depends_on = [aws_ecs_cluster.yurb_dev_ecs_cluster]

  launch_template {
    id      = aws_launch_template.yurb_dev_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "AmazonECSManaged"
    value               = true
    propagate_at_launch = true
  }
}

resource "aws_ecs_cluster" "yurb_dev_ecs_cluster" {
  name = "${var.stack_name}${title(var.stack_environment)}"

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}

resource "aws_ecs_capacity_provider" "yurb_dev_capacity_provider" {
  name = "${var.stack_name}_CapacityProvider_${var.stack_environment}"

  auto_scaling_group_provider {
    auto_scaling_group_arn = aws_autoscaling_group.yurb_dev_ecs_asg.arn

    managed_scaling {
      status                 = "ENABLED"
      target_capacity        = 100
      instance_warmup_period = 300
    }
  }

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}

resource "aws_ecs_cluster_capacity_providers" "yurb_dev_ecs_cluster_capacity_providers" {
  cluster_name = aws_ecs_cluster.yurb_dev_ecs_cluster.name

  capacity_providers = [aws_ecs_capacity_provider.yurb_dev_capacity_provider.name]

  default_capacity_provider_strategy {
    base              = 0
    capacity_provider = aws_ecs_capacity_provider.yurb_dev_capacity_provider.name
    weight            = 1
  }
}

resource "aws_cloudwatch_log_group" "task_log_group" {
  name = "/ecs/${var.stack_name}${local.stack_env_title}"

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}

data "aws_iam_policy_document" "trusted_ecs_task_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "app_task_execution_role" {
  name               = "${var.stack_name}_ECSTaskExecutionRole_${local.stack_env_title}"
  assume_role_policy = data.aws_iam_policy_document.trusted_ecs_task_policy.json
}

resource "aws_iam_role_policy_attachment" "attach_task_er_managed_policy" {
  role       = aws_iam_role.app_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "app_task_role" {
  name               = "${var.stack_name}_ECSTaskRole_${local.stack_env_title}"
  assume_role_policy = data.aws_iam_policy_document.trusted_ecs_task_policy.json

  inline_policy {
    name = "AllowS3Basic"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "s3:PutObject",
            "s3:GetObject",
            "s3:ListBucket",
            "s3:DeleteObject",
            "s3:PutObjectAcl"
          ]
          Resource = [
            "arn:aws:s3:::${var.cdn_bucket_name}/*",
            "arn:aws:s3:::${var.cdn_bucket_name}"
          ]
        }
      ]
    })
  }
}

resource "aws_ecs_task_definition" "app_task_definition" {
  depends_on = [aws_db_instance.app_db_instance, aws_cloudwatch_log_group.task_log_group]

  family                   = "${var.stack_name}_TaskDefinition_${local.stack_env_title}"
  cpu                      = 410
  memory                   = 381 # 0.4GB
  network_mode             = "bridge"
  requires_compatibilities = ["EC2"]
  execution_role_arn       = aws_iam_role.app_task_execution_role.arn
  task_role_arn            = aws_iam_role.app_task_role.arn

  container_definitions = jsonencode([
    {
      name              = var.td_container_name
      image             = var.td_docker_image
      memory            = 378
      memoryReservation = 238
      essential         = true
      portMappings = [
        {
          appProtocol   = "http"
          containerPort = var.td_container_port
          hostPort      = 0
        }
      ]

      environment = [
        {
          name  = "DATABASE_URI"
          value = "postgresql://${var.rds_username}:${var.rds_password}@${aws_db_instance.app_db_instance.address}/${aws_db_instance.app_db_instance.db_name}"
        },
        {
          name  = "AWS_S3_BUCKET"
          value = var.cdn_bucket_name
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/${var.stack_name}${local.stack_env_title}"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
          awslogs-create-group  = "true"
        }
      }
    }
  ])

  tags = {
    environment = var.stack_environment
    project     = var.stack_name
  }
}

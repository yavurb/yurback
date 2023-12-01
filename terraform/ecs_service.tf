data "aws_iam_role" "ecs_service_role" {
  name = "AWSServiceRoleForECS"
}

resource "aws_ecs_service" "app_ecs_service" {
  name                               = "${var.stack_name}_BackendService_${local.stack_env_title}"
  cluster                            = aws_ecs_cluster.app_ecs_cluster.id
  task_definition                    = aws_ecs_task_definition.app_task_definition.arn
  desired_count                      = 1
  health_check_grace_period_seconds  = 30
  iam_role                           = data.aws_iam_role.ecs_service_role.arn
  force_new_deployment               = true
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  ordered_placement_strategy {
    type  = "binpack"
    field = "memory"
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app_lb_target_group.arn
    container_name   = var.td_container_name
    container_port   = var.td_container_port
  }

  capacity_provider_strategy {
    base              = 0
    capacity_provider = aws_ecs_capacity_provider.app_capacity_provider.name
    weight            = 1
  }

  deployment_controller {
    type = "ECS"
  }

  triggers = {
    redeployment = timestamp()
  }

  depends_on = [aws_autoscaling_group.app_ecs_asg]
}

resource "aws_appautoscaling_target" "app_service_autoscaling_target" {
  max_capacity       = 2
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.app_ecs_cluster.name}/${aws_ecs_service.app_ecs_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "ecs_policy" {
  name               = "scale_dynamically"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.app_service_autoscaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.app_service_autoscaling_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.app_service_autoscaling_target.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value = 80

    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}
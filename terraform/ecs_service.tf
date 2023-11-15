data "aws_iam_role" "ecs_service_role" {
  name = "AWSServiceRoleForECS"
}

resource "aws_ecs_service" "yurb_dev_ecs_service" {
  name                              = "${var.stack_name}_BackendService_${var.stack_environment}"
  cluster                           = aws_ecs_cluster.yurb_dev_ecs_cluster.id
  task_definition                   = aws_ecs_task_definition.yurb_dev_tf.arn
  desired_count                     = 1
  force_new_deployment              = var.force_deploy
  health_check_grace_period_seconds = 30
  iam_role                          = data.aws_iam_role.ecs_service_role.arn
  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  ordered_placement_strategy {
    type  = "binpack"
    field = "memory"
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.yurb_dev_lb_tg.arn
    container_name   = var.td_container_name
    container_port   = var.td_container_port
  }

  capacity_provider_strategy {
    base              = 0
    capacity_provider = aws_ecs_capacity_provider.yurb_dev_capacity_provider.name
    weight            = 1
  }

  deployment_controller {
    type = "ECS"
  }

  triggers = {
    redeployment = timestamp()
  }

  depends_on = [aws_autoscaling_group.yurb_dev_ecs_asg]
}

resource "aws_appautoscaling_target" "yurb_dev_service_autoscaling_target" {
  max_capacity       = 2
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.yurb_dev_ecs_cluster.name}/${aws_ecs_service.yurb_dev_ecs_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "ecs_policy" {
  name               = "scale_dynamically"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.yurb_dev_service_autoscaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.yurb_dev_service_autoscaling_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.yurb_dev_service_autoscaling_target.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value = 80

    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}
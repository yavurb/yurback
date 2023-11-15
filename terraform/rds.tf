resource "aws_db_instance" "yurb_dev_db_instance" {
  identifier             = var.rds_identifier
  allocated_storage      = 20
  instance_class         = "db.t3.micro"
  engine                 = "postgres"
  engine_version         = "15.3"
  username               = var.rds_username
  password               = var.rds_password
  db_name                = var.rds_db_name
  vpc_security_group_ids = [aws_security_group.allow_app_traffic.id]
  skip_final_snapshot    = true
  publicly_accessible    = true
}

resource "aws_security_group" "allow_app_traffic" {
  name        = "${var.stack_name}_RDSInstance_${var.stack_environment}"
  description = "Allow only inbound traffic from the backend app"
  vpc_id      = aws_default_vpc.default.id

  egress = []

  tags = {
    Name = "allow_${var.stack_name}_traffic"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_yurb_dev_container_instances" {
  security_group_id            = aws_security_group.allow_app_traffic.id
  referenced_security_group_id = aws_security_group.allow_components_traffic.id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}

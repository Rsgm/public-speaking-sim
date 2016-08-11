resource "aws_launch_configuration" "worker_config" {
  image_id = "${var.worker_ami}"
  instance_type = "t2.nano"
  security_groups = [
    "${aws_security_group.worker.id}",
    "${aws_security_group.ssh.id}"
  ]
  key_name = "Ryan's desktop"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "worker_scale" {
  name = "worker_scale"
  vpc_zone_identifier = [
    "${aws_subnet.worker_subnet.id}"
  ]

  // todo: up this to 50 when it is proven working
  max_size = 8
  min_size = 2
  //  health_check_grace_period = 300
  //  health_check_type = "ELB"
  launch_configuration = "${aws_launch_configuration.worker_config.name}"
}


// worker scaling policies.
resource "aws_autoscaling_policy" "worker_scale_policy_up" {
  name = "worker-scale-cpu-up"
  scaling_adjustment = 100
  adjustment_type = "PercentChangeInCapacity"
  cooldown = 60
  autoscaling_group_name = "${aws_autoscaling_group.worker_scale.name}"
}

resource "aws_autoscaling_policy" "worker_scale_policy_down" {
  name = "worker-scale-cpu-down"
  scaling_adjustment = -50
  adjustment_type = "PercentChangeInCapacity"
  cooldown = 60
  autoscaling_group_name = "${aws_autoscaling_group.worker_scale.name}"
}


// worker scaling alarms
resource "aws_cloudwatch_metric_alarm" "worker_alarm_cpu_high" {
  alarm_name = "worker-alarm-cpu-high"
  namespace = "AWS/EC2"

  metric_name = "CPUUtilization"
  comparison_operator = "GreaterThanThreshold"
  threshold = "81"
  statistic = "Maximum"

  period = "60"
  evaluation_periods = "1"

  dimensions {
    AutoScalingGroupName = "${aws_autoscaling_group.worker_scale.name}"
  }

  alarm_description = "Monitor workers for high cpu use"
  alarm_actions = [
    "${aws_autoscaling_policy.worker_scale_policy_up.arn}"]
}

resource "aws_cloudwatch_metric_alarm" "worker_alarm_cpu_low" {
  alarm_name = "worker-alarm-cpu-low"
  namespace = "AWS/EC2"

  metric_name = "CPUUtilization"
  comparison_operator = "LessThanThreshold"
  statistic = "Maximum"
  threshold = "60"
  // todo: optimize these values and times

  period = "60"
  evaluation_periods = "2"

  dimensions {
    AutoScalingGroupName = "${aws_autoscaling_group.worker_scale.name}"
  }

  alarm_description = "Monitor workers for high cpu use"
  alarm_actions = [
    "${aws_autoscaling_policy.worker_scale_policy_down.arn}"
  ]
}


resource "aws_security_group" "worker" {
  name = "worker"
  description = "Worker security group"
  vpc_id = "${aws_vpc.speakeazy_vpc.id}"
  // ftp
  egress {
    from_port = 20
    to_port = 20
    protocol = "tcp"
    cidr_blocks = [
      "${var.nginx_ip}/32"
    ]
  }
  // db
  egress {
    from_port = "${var.db_port}"
    to_port = "${var.db_port}"
    protocol = "tcp"
    cidr_blocks = [
      "${var.main_block}"
    ]
  }
  // redis
  egress {
    from_port = "${var.redis_port}"
    to_port = "${var.redis_port}"
    protocol = "tcp"
    cidr_blocks = [
      "${var.docker_ip}/32"
    ]
  }
  // https - PUBLIC
  egress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
  tags {
    Name = "worker"
  }
}

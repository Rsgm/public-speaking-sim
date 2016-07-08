provider "aws" {
  region = "us-east-1"
}

variable "django_ami" {
  default = "ami-f169eee6"
}
variable "nginx_ami" {
  default = "ami-c268efd5"
}
variable "docker_ami" {
  default = "ami-a88a46c5"
}
variable "worker_ami" {
  default = "ami-966aed81"
}
variable "ssh_key" {
  default = "Ryan's desktop"
}

variable "gunicorn_port" {
  default = 5000
}
variable "redis_port" {
  default = 6379
}
variable "db_port" {
  default = 3306
}


// IPs
variable "nginx_ip" {
  default = "10.0.1.4"
}
variable "docker_ip" {
  default = "10.0.1.5"
}
variable "django_ip" {
  default = "10.0.1.6"
}

// VPC ips
variable "vpc_block" {
  default = "10.0.0.0/16"
}
variable "main_block" {
  default = "10.0.1.0/24"
}
variable "worker_block" {
  default = "10.0.2.0/24"
}


// VPC
// =========
resource "aws_vpc" "speakeazy_vpc" {
  cidr_block = "${var.vpc_block}"
  tags {
    Name = "speakeazy vpc"
  }
}
resource "aws_subnet" "main_subnet" {
  vpc_id = "${aws_vpc.speakeazy_vpc.id}"
  cidr_block = "${var.main_block}"
  tags {
    Name = "main subnet"
  }
}
resource "aws_subnet" "worker_subnet" {
  vpc_id = "${aws_vpc.speakeazy_vpc.id}"
  cidr_block = "${var.worker_block}"
  tags {
    Name = "worker subnet"
  }
}

resource "aws_internet_gateway" "vpc_gateway" {
  vpc_id = "${aws_vpc.speakeazy_vpc.id}"

  tags {
    Name = "speakeazy"
  }
}
resource "aws_route_table" "route_table" {
  vpc_id = "${aws_vpc.speakeazy_vpc.id}"
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.vpc_gateway.id}"
  }
}
resource "aws_route_table_association" "eu-west-1a-private" {
    subnet_id = "${aws_subnet.main_subnet.id}"
    route_table_id = "${aws_route_table.route_table.id}"
}



// Public Ips
// ==========
resource "aws_eip_association" "nginx_static_ip" {
  instance_id = "${aws_instance.nginx.id}"
  allocation_id = "eipalloc-1d473965"
}


// Nginx, docker, and django single instances
// =========================================
resource "aws_instance" "nginx" {
  ami = "${var.nginx_ami}"
  instance_type = "t2.nano"
  vpc_security_group_ids = [
    "${aws_security_group.nginx.id}",
    "${aws_security_group.ssh.id}"
  ]
  subnet_id = "${aws_subnet.main_subnet.id}"
  private_ip = "${var.nginx_ip}"
  key_name = "Ryan's desktop"
  tags {
    Name = "nginx"
  }
}
//resource "aws_instance" "docker" {
//  ami = "${var.docker_ami}"
//  instance_type = "t2.nano"
//  vpc_security_group_ids = [
//    "${aws_security_group.docker.id}",
//    "${aws_security_group.ssh.id}"
//  ]
//  subnet_id = "${aws_subnet.main_subnet.id}"
//  private_ip = "${var.docker_ip}"
//  iam_instance_profile = "${aws_iam_instance_profile.docker_ecs.name}"
//  key_name = "Ryan's desktop"
//
//  tags {
//    Name = "docker"
//  }
//
//  provisioner "file" {
//    source = "files/docker/ecs.config"
//    destination = "/etc/ecs/ecs.config"
//  }
//}
resource "aws_instance" "django" {
  ami = "${var.django_ami}"
  instance_type = "t2.micro"
  vpc_security_group_ids = [
    "${aws_security_group.django.id}",
    "${aws_security_group.ssh.id}"
  ]
  subnet_id = "${aws_subnet.main_subnet.id}"
  private_ip = "${var.django_ip}"
  key_name = "Ryan's desktop"
  tags {
    Name = "django"
  }
}


// Docker iam
resource "aws_iam_instance_profile" "docker_ecs" {
    name = "test_profile"
    roles = ["ecsInstanceRole"]
}


// Security Groups
// ===============
resource "aws_security_group" "ssh" {
  name = "ssh"
  description = "public ssh access"
  vpc_id = "${aws_vpc.speakeazy_vpc.id}"
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
  tags {
    Name = "ssh"
  }
}
resource "aws_security_group" "nginx" {
  name = "nginx"
  description = "Allow nginx web traffic"
  vpc_id = "${aws_vpc.speakeazy_vpc.id}"
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
  // django
  egress {
    from_port = "${var.gunicorn_port}"
    to_port = "${var.gunicorn_port}"
    protocol = "tcp"
    cidr_blocks = [
      "${var.django_ip}/32"
    ]
  }
  // Allow 443 traffic for certbot - PUBLIC
  egress {
    from_port = "443"
    to_port = "443"
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
  tags {
    Name = "nginx"
  }
}
resource "aws_security_group" "docker" {
  name = "docker"
  description = "Allow docker on the vpc only"
  vpc_id = "${aws_vpc.speakeazy_vpc.id}"
  ingress {
    from_port = "${redis_port}"
    to_port = "${redis_port}"
    protocol = "tcp"
    cidr_blocks = [
      "${var.vpc_block}"
    ]
  }
  tags {
    Name = "docker"
  }
}
resource "aws_security_group" "django" {
  name = "django"
  description = "Django security group"
  vpc_id = "${aws_vpc.speakeazy_vpc.id}"
  // gunicorn
  ingress {
    from_port = "${var.gunicorn_port}"
    to_port = "${var.gunicorn_port}"
    protocol = "tcp"
    cidr_blocks = [
      "${var.nginx_ip}/32"
    ]
  }
  // ftp
  ingress {
    from_port = 20
    to_port = 20
    protocol = "tcp"
    cidr_blocks = [
      "${var.worker_block}"
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
  // email - PUBLIC
  egress {
    from_port = 587
    to_port = 587
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
  tags {
    Name = "django"
  }
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
    Name = "django"
  }
}

// File Storage
resource "aws_s3_bucket" "bucket" {
  bucket = "speakeazy-upgrade-test"
  // todo: change this
  acl = "private"
}


// Worker autoscaling config
// =========================
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


// Docker
// for small tools that don't need much resouces
// =============================================
resource "aws_ecs_cluster" "docker_tools" {
  name = "tools"
}

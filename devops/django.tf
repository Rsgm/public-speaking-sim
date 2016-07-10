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

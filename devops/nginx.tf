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

resource "aws_eip_association" "nginx_static_ip" {
  instance_id = "${aws_instance.nginx.id}"
  allocation_id = "eipalloc-1d473965"
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

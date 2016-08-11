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

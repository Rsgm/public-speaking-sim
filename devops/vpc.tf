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

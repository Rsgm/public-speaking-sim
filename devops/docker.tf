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
//
//resource "aws_ecs_cluster" "docker_tools" {
//  name = "tools"
//}
//
//resource "aws_iam_instance_profile" "docker_ecs" {
//    name = "dockerEcs"
//    roles = ["ecsInstanceRole"]
//}
//
//
//resource "aws_security_group" "docker" {
//  name = "docker"
//  description = "Allow docker on the vpc only"
//  vpc_id = "${aws_vpc.speakeazy_vpc.id}"
//  ingress {
//    from_port = "${redis_port}"
//    to_port = "${redis_port}"
//    protocol = "tcp"
//    cidr_blocks = [
//      "${var.vpc_block}"
//    ]
//  }
//  tags {
//    Name = "docker"
//  }
//}

// AMIs
variable "django_image" {
}
variable "nginx_image" {
}
variable "worker_image" {
}


variable "ssh_key" {
}


// Ports
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
//variable "docker_ip" {
//  default = "10.0.1.5"
//}
variable "django_ip" {
  default = "10.0.1.6"
}
variable "worker_ip" {
  default = "10.0.1.6"
}


// VPC ips
variable "vpc_block" {
  default = "10.0.0.0/16"
}
variable "main_block" {
  default = "10.0.1.0/24"
}
//variable "worker_block" {
//  default = "10.0.2.0/24"
//}

// File Storage
resource "aws_s3_bucket" "bucket" {
  bucket = "speakeazy-upgrade-test"
  // todo: change this
  acl = "private"
}

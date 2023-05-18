terraform {
  backend "s3" {
    bucket         = "terraform-state-s3-store"
    key            = "./terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "tf-state-locks"
  }
}

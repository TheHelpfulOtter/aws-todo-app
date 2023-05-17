
terraform {
  backend "s3" {
    bucket  = "plutus-tf-dev"
    encrypt = true
    key     = "./terraform.tfstate"
    region  = "af-south-1"
  }
}
  

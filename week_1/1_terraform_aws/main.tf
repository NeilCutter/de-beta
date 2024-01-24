terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.33.0"
    }
  }
}

provider "aws" {
  region     = "us-east-1"
  access_key = "my-access-key"
  secret_key = "my-secret-key"
}

resource "aws_s3_bucket" "demo-bucket" {
  bucket = "terraform-demo-1123-terra-bucket"

  tags = {
    Name = "My bucket"
  }
}
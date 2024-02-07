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
  access_key = "My-Access-Key"
  secret_key = "My-Secret-Key"
}

resource "aws_s3_bucket" "demo-bucket" {
  bucket = var.aws_bucket

  tags = {
    Name = var.aws_bucker_name
  }
}

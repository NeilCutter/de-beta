terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}
#Creating AWS s3 Bucket
resource "aws_s3_bucket" "data-lake" {
  bucket        = var.bucket_name
  force_destroy = "true"
}
#Creating AWS redshift cluster
resource "aws_redshift_cluster" "data-warehouse" {
  cluster_identifier  = var.cluster_identifier
  database_name       = var.dbname
  master_username     = var.dbuser
  master_password     = var.dbpassword
  node_type           = "dc2.large"
  cluster_type        = "single-node"
  skip_final_snapshot = "true" #necessary if you want to destroy
}


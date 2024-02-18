#This is for demo purposes. This should be in gitignore file
variable "bucket_name" {
    description = "Week-2 Data Lake"
    default = "de-zoomcamp-bucket"
}
variable "cluster_identifier" {
    description = "Week-2 Data Warehouse"
    default = "test-cluster"
}
variable "dbname" {
    description = "Database name"
    default = "dev"
}
variable "dbuser" {
    description = "Database username"
    default = "user"
}
variable "dbpassword" {
    description = "Database password"
    default = "password"
}
variable "aws_region" {
  description = "AWS region where the VPC and EKS cluster are provisioned."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name prefix applied to every created resource."
  type        = string
  default     = "medidesk"
}

variable "environment" {
  description = "Deployment environment label (dev/staging/prod)."
  type        = string
  default     = "dev"
}

variable "cluster_version" {
  description = "Kubernetes version for the EKS control plane."
  type        = string
  default     = "1.31"
}

variable "node_instance_type" {
  description = "EC2 instance type for the EKS managed node group."
  type        = string
  default     = "t3.medium"
}

variable "node_min_size" {
  description = "Minimum number of worker nodes."
  type        = number
  default     = 1
}

variable "node_desired_size" {
  description = "Desired number of worker nodes."
  type        = number
  default     = 2
}

variable "node_max_size" {
  description = "Maximum number of worker nodes."
  type        = number
  default     = 3
}

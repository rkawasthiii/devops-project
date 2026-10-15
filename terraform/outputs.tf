output "cluster_name" {
  description = "Name of the provisioned EKS cluster."
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "HTTPS endpoint of the EKS control plane."
  value       = module.eks.cluster_endpoint
}

output "cluster_region" {
  description = "AWS region the cluster lives in."
  value       = var.aws_region
}

output "vpc_id" {
  description = "ID of the created VPC."
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet IDs."
  value       = module.vpc.public_subnets
}

output "private_subnet_ids" {
  description = "Private subnet IDs."
  value       = module.vpc.private_subnets
}

output "configure_kubectl" {
  description = "Command to point kubectl at the new cluster."
  value       = "aws eks update-kubeconfig --name ${module.eks.cluster_name} --region ${var.aws_region}"
}

variable "aws_region" {
  type        = string
  default     = "eu-west-1"
  description = "AWS region to deploy into"
}

variable "app_name" {
  type        = string
  default     = "meal-grocery-planner"
}

variable "docker_image" {
  type        = string
  description = "Docker image URL in ECR (with tag)"
}

variable "vpc_id" {
  type        = string
  description = "The VPC id for ECS"
}

variable "subnets" {
  type        = list(string)
  description = "Public subnets for ALB and ECS tasks"
}
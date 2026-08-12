variable "aws_region" {
  description = "AWS region for the lab"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Resource name prefix"
  type        = string
  default     = "sre-observability-lab"
}

variable "container_image" {
  description = "Container image deployed to ECS. Replace with your ECR image for a real deployment."
  type        = string
  default     = "public.ecr.aws/docker/library/nginx:alpine"
}

variable "desired_count" {
  description = "Number of ECS tasks"
  type        = number
  default     = 2
}

resource "aws_ecr_repository" "todo_app_ecr" {
  name                 = var.repository_name
  image_tag_mutability = "MUTABLE"
}


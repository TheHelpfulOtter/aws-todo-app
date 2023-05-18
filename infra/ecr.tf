resource "aws_ecr_repository" "to_do_app_ecr" {
  name                 = "aws-todo-app"
  image_tag_mutability = "MUTABLE"
}

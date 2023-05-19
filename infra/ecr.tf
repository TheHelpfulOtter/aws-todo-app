resource "aws_ecr_repository" "todo_app_ecr" {
  name                 = "aws-todo-app"
  image_tag_mutability = "MUTABLE"
}

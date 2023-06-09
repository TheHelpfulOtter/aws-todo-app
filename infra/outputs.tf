output "dynamodb_table_name" {
  value = aws_dynamodb_table.tasks_table.name
}

output "image_uri" {
  description = ""
  value       = "${aws_ecr_repository.todo_app_ecr.repository_url}:${local.latest_tag}"
}

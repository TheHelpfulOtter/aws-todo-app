output "dynamodb_table_name" {
  value = aws_dynamodb_table.tasks_table.name
}

output "tag" {
  description = ""
  value       = jsondecode(data.external.latest_tag.result.tags)
}

# Source: https://github.com/hashicorp/terraform-provider-aws/issues/12798
# Terraform's AWS provider does not provide a mechanism to query the ecr repository.
#
# We use an external data source, which can run any program that returns valid JSON, to run the AWS
# cli manually, which will produce a JSON in the following format:
#
#   {
#     "tags": "[\"1.0.0.1166\"]"
#   }
#
data "external" "latest_tag" {
  program = [
    "aws", "ecr", "describe-images",
    "--repository-name", var.repository_name,
    "--query", "{\"tags\": to_string(sort_by(imageDetails,& imagePushedAt)[-1].imageTags)}",
  ]
}

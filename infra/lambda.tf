################################################################################################
# Lambda Function (LF) to run container from ECR
################################################################################################

resource "aws_lambda_function" "todo_lambda" {
  function_name = "todo-lambda"
  role          = aws_iam_role.todo_lambda_role.arn
  #   handler       = "main.handler"  # Not needed for images
  #   runtime       = "python3.10"  # Not needed for images
  package_type = "Image"
  image_uri    = "${aws_ecr_repository.todo_app_ecr.repository_url}:${local.latest_tag}"
  timeout      = 60
  memory_size  = 1536
}

locals {
  latest_tag = trim(data.external.latest_tag.result.tags, "[]\"")
}

################################################################################################
# Lambda Function (LF) roles
################################################################################################

# Lambda execution role
data "aws_iam_policy_document" "assume_role_lambda" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "todo_lambda_role" {
  name               = "todo-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_lambda.json
}

resource "aws_iam_role_policy_attachment" "assume_role_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.todo_lambda_role.name
}

# Give permission to use DynamoDB
resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  role       = aws_iam_role.todo_lambda_role.name
}

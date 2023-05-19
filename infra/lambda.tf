################################################################################################
# Lambda Function (LF) to run container from ECR
################################################################################################
resource "aws_iam_role" "todo_lambda_role" {
  name               = "todo-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_lambda
}

resource "aws_iam_role_policy_attachment" "todo_lambda_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.todo_lambda_role.name
}

resource "aws_lambda_function" "todo_lambda" {
  function_name = "todo-lambda"
  role          = aws_iam_role.todo_lambda_role.arn
  #   handler       = "main.handler"  # Not needed for images
  #   runtime       = "python3.10"  # Not needed for images
  package_type = "Image"
  image_uri    = aws_ecr_repository.todo_app_ecr.repository_url
  timeout      = 30
  memory_size  = 1536
}




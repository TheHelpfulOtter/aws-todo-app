resource "aws_api_gateway_rest_api" "api_gw" {
  name = "todo-api-gateway"
}

resource "aws_api_gateway_resource" "api_gw_resource" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  parent_id   = aws_api_gateway_rest_api.api_gw.root_resource_id
  path_part   = "api_gw-resource"
}

resource "aws_api_gateway_method" "api_gw_method" {
  rest_api_id   = aws_api_gateway_rest_api.api_gw.id
  resource_id   = aws_api_gateway_resource.api_gw_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "api_gw_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api_gw.id
  resource_id             = aws_api_gateway_resource.api_gw_resource.id
  http_method             = aws_api_gateway_method.api_gw_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.todo_lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "api_gw_deployment" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  stage_name  = "dev"
}

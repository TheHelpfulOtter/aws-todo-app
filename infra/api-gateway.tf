resource "aws_api_gateway_rest_api" "api_gw" {
  name = "todo-api-gateway"
}

# resource "aws_api_gateway_resource" "api_gw_resource_root" {
#   rest_api_id = aws_api_gateway_rest_api.api_gw.id
#   parent_id   = aws_api_gateway_rest_api.api_gw.root_resource_id
#   path_part   = "/"
# }

resource "aws_api_gateway_resource" "api_gw_resource_proxy" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id
  parent_id   = aws_api_gateway_rest_api.api_gw.root_resource_id
  path_part   = "{proxy+}"
}

# resource "aws_api_gateway_method" "api_gw_method_root" {
#   rest_api_id   = aws_api_gateway_rest_api.api_gw.id
#   resource_id   = aws_api_gateway_resource.api_gw_resource.id
#   http_method   = "ANY"
#   authorization = "NONE"
# }

resource "aws_api_gateway_method" "api_gw_method_proxy" {
  rest_api_id   = aws_api_gateway_rest_api.api_gw.id
  resource_id   = aws_api_gateway_resource.api_gw_resource_proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "api_gw_integ_proxy" {
  rest_api_id             = aws_api_gateway_rest_api.api_gw.id
  resource_id             = aws_api_gateway_resource.api_gw_resource_proxy.id
  http_method             = aws_api_gateway_method.api_gw_method_proxy.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.todo_lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "api_gw_deploy" {
  rest_api_id = aws_api_gateway_rest_api.api_gw.id

  # Allow for redeployment if changes are made to apigw resources
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.api_gw_resource_proxy.id,
      aws_api_gateway_method.api_gw_method_proxy.id,
      aws_api_gateway_integration.api_gw_integ_proxy.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "api_gw_stage" {
  deployment_id = aws_api_gateway_deployment.api_gw_deploy.id
  rest_api_id   = aws_api_gateway_rest_api.api_gw.id
  stage_name    = "dev"
}

# Give apigw permission to access lambda function
resource "aws_lambda_permission" "api_gw_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.todo_lambda.arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.api_gw.execution_arn}/*/*/*"
}

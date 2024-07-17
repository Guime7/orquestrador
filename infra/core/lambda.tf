##create iam role for lambda read sqs, putevent and putlogevents
resource "aws_iam_role" "lambda_role" {
  name = "orquestrador-cargas-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_policy" {
  name = "orquestrador-cargas-policy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes",
        "sqs:SendMessage",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "events:PutEvents"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

##zip code in app folder and send to lambda
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.cwd}/../app"
  output_path = "${path.cwd}/../lambda.zip"
}

### create lambda function trigger by sqs queue
resource "aws_lambda_function" "lambda_function" {
  function_name = "orquestrador-cargas"
  handler = "lambda.handler"
  runtime = "python3.10"
  role = aws_iam_role.lambda_role.arn
  filename = "lambda.zip"
source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  depends_on = [aws_sqs_queue.sqs_queue]
}

resource "aws_lambda_event_source_mapping" "lambda_event_source_mapping" {
  event_source_arn = aws_sqs_queue.sqs_queue.arn
  function_name    = aws_lambda_function.lambda_function.arn
  batch_size       = 1 #10
  maximum_batching_window_in_seconds = 10 #60
#   scaling_config = {
#     maximum_concurrency = 3
#   }
}
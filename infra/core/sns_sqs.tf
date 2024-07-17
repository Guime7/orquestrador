
### create sqs queue   
resource "aws_sqs_queue" "sqs_queue" {
  name = "orquestrador-cargas"
}

### create sns topic
resource "aws_sns_topic" "sns_topic" {
  name = "acl-sucesso"
}

### create sns subscription
resource "aws_sns_topic_subscription" "sns_subscription" {
  topic_arn = aws_sns_topic.sns_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.sqs_queue.arn
}
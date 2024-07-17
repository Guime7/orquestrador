### create log group
resource "aws_cloudwatch_log_group" "log_group_table" {
  name              = "/tabelas-carregadas"
  retention_in_days = 30
}


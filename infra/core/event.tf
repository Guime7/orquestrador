##log group 
resource "aws_cloudwatch_log_group" "log_group_event" {
  name              = "/load-events"
  retention_in_days = 30
}

##create event bus
resource "aws_cloudwatch_event_bus" "event_bus" {
    name = "orquestrador-cargas"
}

### event rule load event data in log group - any event
resource "aws_cloudwatch_event_rule" "event_rule" {
    name                = "load-event-data"
    event_pattern       = "{}"
    event_bus_name      = aws_cloudwatch_event_bus.event_bus.name
}

### event target to log group
resource "aws_cloudwatch_event_target" "event_target" {
    rule      = aws_cloudwatch_event_rule.event_rule.name
    target_id = "log_group_event"
    arn       = aws_cloudwatch_log_group.log_group_event.arn
}
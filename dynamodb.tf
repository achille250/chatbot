provider "aws" {
  region     = "us-east-1"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "chatbot"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "user_input"
  range_key      = "assistant_reply"

  attribute {
    name = "user_input"
    type = "S"
  }

  attribute {
    name = "assistant_reply"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }

  global_secondary_index {
    name               = "UserTitleIndex"
    hash_key           = "user_input"
    range_key          = "assistant_reply"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["user_input"]
  }

  tags = {
    Name        = "dynamodb-table"
    Environment = "Training"
  }
}
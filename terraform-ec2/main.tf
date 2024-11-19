provider "aws" {
  region = "ap-southeast-1"
}

# Default VPC
data "aws_vpc" "default" {
  default = true
}

# Fetch a default subnet for a specific Availability Zone
data "aws_subnet" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

  filter {
    name   = "default-for-az"
    values = ["true"]
  }

  # Specify an availability zone
  filter {
    name   = "availability-zone"
    values = ["ap-southeast-1a"]
  }
}


# Security group to allow SSH and HTTP/HTTPS
resource "aws_security_group" "dev_sg" {
  name        = "dev-server-sg"
  description = "Allow SSH, HTTP, and HTTPS"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance
resource "aws_instance" "terraform-mehraj-autoquery-dev" {
  ami           = "ami-0aa097a5c0d31430a"
  instance_type = "t3.small"

  tags = {
    Name = "terraform-mehraj-autoquery-dev"
  }

  associate_public_ip_address = true
  subnet_id                   = data.aws_subnet.default.id
  key_name                    = "mehraj-auto-query"

  vpc_security_group_ids = [aws_security_group.dev_sg.id]
}

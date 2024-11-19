ssh -i mehraj-auto-query.pem ec2-user@13.212.177.252

aws ec2 create-key-pair --key-name my-key-pair --query 'KeyMaterial' --output text > my-key-pair.pem
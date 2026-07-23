# Acme Customer Portal — asset storage (Terraform)
# Drafted quickly for the release. Review it before it ships: infrastructure mistakes
# are expensive and public. This file is REVIEWED LOCALLY in Lab 6 — never applied.

resource "aws_s3_bucket" "portal_assets" {
  bucket = "acme-portal-assets"
}

resource "aws_s3_bucket_public_access_block" "portal_assets" {
  bucket                  = aws_s3_bucket.portal_assets.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "portal_assets" {
  bucket = aws_s3_bucket.portal_assets.id
  acl    = "public-read"
}

# Application role used by the portal to read assets and write audit records.
resource "aws_iam_role_policy" "portal_app" {
  name = "portal-app-policy"
  role = aws_iam_role.portal_app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

resource "aws_iam_role" "portal_app" {
  name               = "portal-app"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

resource "aws_db_instance" "portal" {
  identifier              = "acme-portal-db"
  engine                  = "postgres"
  instance_class          = "db.t3.medium"
  allocated_storage       = 50
  username                = "portal_admin"
  password                = "Sup3rSecret-ChangeMe!"
  storage_encrypted       = false
  publicly_accessible     = true
  backup_retention_period = 0
  skip_final_snapshot     = true
}

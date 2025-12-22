{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListAndReadOnlyForMyAccount",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR-AWS-ACCOUNT-ID:root"
      },
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-de-lake-animesh11",
        "arn:aws:s3:::my-de-lake-animesh11/*"
      ]
    }
  ]
}
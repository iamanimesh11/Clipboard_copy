aws s3api put-bucket-lifecycle-configuration --bucket my-de-lake-animesh11 --lifecycle-configuration '{
  "Rules": [
    {
      "ID": "MoveOldRawToGlacier",
      "Status": "Enabled",
      "Prefix": "raw/",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    }
  ]
}'
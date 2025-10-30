                        ┌───────────────────────────────────────────┐
                        │        Microservices / APIs               │
                        │───────────────────────────────────────────│
                        │  • OrderService → {"order_id":123,...}    │
                        │  • UserService  → {"user_id":42,...}      │
                        │  • InventoryService → {"sku":"A123",...}  │
                        └───────────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────┐
│ Step 1: Amazon S3 Landing Bucket                                   │
│  • Receives raw JSON payloads from multiple microservices           │
│  • Stores data for downstream processing                            │
└────────────────────────────────────────────────────────────────────┘
                                        │
                          (S3 upload event triggers)
                                        ▼
┌────────────────────────────────────────────────────────────────────┐
│ Step 2: AWS Lambda                                                  │
│  • Validates JSON schema                                            │
│  • Tags metadata dynamically                                        │
│  • Moves validated data to curated bucket                           │
└────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────┐
│ Step 3: Amazon S3 Curated Bucket                                   │
│  • Stores cleaned & validated data                                  │
│  • AWS Glue Crawler auto-detects new partitions                     │
└────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────┐
│ Step 4: AWS Glue Data Catalog                                       │
│  • Updates schema & metadata catalog                                │
│  • Data available for:                                              │
│       - Amazon Athena                                               │
│       - Amazon Redshift Spectrum                                    │
└────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────┐
│ Step 5: S3 Lifecycle Policy                                         │
│  • Moves older data → Amazon S3 Glacier for cost optimization       │
└────────────────────────────────────────────────────────────────────┘

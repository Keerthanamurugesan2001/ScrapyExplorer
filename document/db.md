To save the dataset is being captured to s3:

Save Credential:

```
export AWS_ACCESS_KEY_ID='your_access_key_id'
export AWS_SECRET_ACCESS_KEY='your_secret_access_key'
```

To save the extracted data to local:

```
scrapy crawl chocolate_itemloader -o output.csv
```

Once verified, manually upload the CSV to S3 using:

```
aws s3 cp output.csv s3://chocolatescrapper/myscrapeddata.csv
```
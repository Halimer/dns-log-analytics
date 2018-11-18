CREATE EXTERNAL TABLE IF NOT EXISTS DNS_Analytics.logs (
  `Month` string,
  `Day` int,
  `Time` string,
  `DNSmasq` string,
  `Request_type` string,
  `Domain` string,
  `Action` string,
  `Response` string 
)
PARTITIONED BY (d string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ' ',
  'field.delim' = ' ',
  'collection.delim' = ' ',
  'mapkey.delim' = ' '
) LOCATION 's3://halimer-dns-analytics/'
TBLPROPERTIES ('has_encrypted_data'='false');

MSCK REPAIR TABLE DNS_analytics.logs_partitioned
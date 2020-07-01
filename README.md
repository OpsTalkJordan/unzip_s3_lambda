# unzip_s3_lambda

This function uses event notifications from AWS S3 to extract zip files uploaded to S3 and move them to a target bucket.

> **Note:** This hasn't been tested as of yet at all. Use at your own risk.

## Prerequisites

- [Terraform](https://www.terraform.io/)
- [Python 3.6+](https://www.python.org/)

## Getting Started

Clone the repo.

```bash
$ git clone https://github.com/OpsTalkJordan/unzip_s3_lambda.git
```

> **Note:**  Once you've cloned the repo edit the terraform.tfvars file to set your source and target buckets.

Run `terrform init` to download the provider plugins.

```bash
$ terraform init
```

As a good habit always run `terraform plan` to make sure you're not going to clobber anything.

> **Note:** Ensure you are authenticated to AWS as documented in the [Terraform AWS provider documentation](https://www.terraform.io/docs/providers/aws/index.html)

```bash
$ terraform plan
```

Run `terraform apply` to deploy.

```bash
$ terraform apply
```

## Contributing
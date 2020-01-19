# GitHub Branch Protection

This is a Serverless project that deploys an AWS API Gateway and AWS Lambda function which auto-protects a GitHub branch on repo creation.

## Deploying the project

### 1. Requirements

1. Generate your **GitHub Personal access token** by going to `Settings > Developer settings > Personal access token > Generate new token`. Give your token a descriptive name, like "Github Branch Protect". Give your token full `repo` permissions.
2. Create an **AWS IAM user or role** which will deploy this Serverless project. Your IAM user/role will requirement the following policies:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "lambda:TagResource",
                "logs:DeleteSubscriptionFilter",
                "iam:CreateRole",
                "iam:AttachRolePolicy",
                "iam:PutRolePolicy",
                "cloudformation:ContinueUpdateRollback",
                "logs:CreateLogStream",
                "apigateway:UpdateRestApiPolicy",
                "cloudformation:DescribeStackEvents",
                "iam:DetachRolePolicy",
                "iam:ListAttachedRolePolicies",
                "logs:DeleteRetentionPolicy",
                "cloudformation:UpdateStack",
                "lambda:DeleteFunction",
                "apigateway:GET",
                "cloudformation:DescribeChangeSet",
                "s3:DeleteObject",
                "s3:HeadBucket",
                "iam:ListRolePolicies",
                "cloudformation:ExecuteChangeSet",
                "cloudformation:ListStackResources",
                "iam:ListPolicies",
                "iam:GetRole",
                "iam:GetPolicy",
                "lambda:List*",
                "iam:DeleteRole",
                "logs:CreateLogGroup",
                "cloudformation:DescribeStacks",
                "s3:PutObject",
                "s3:GetObject",
                "logs:PutMetricFilter",
                "cloudformation:GetStackPolicy",
                "cloudformation:GetTemplate",
                "cloudformation:DeleteStack",
                "lambda:PublishVersion",
                "apigateway:POST",
                "logs:PutSubscriptionFilter",
                "lambda:DeleteEventSourceMapping",
                "cloudformation:ValidateTemplate",
                "lambda:CreateAlias",
                "cloudformation:CancelUpdateStack",
                "s3:DeleteObjectVersion",
                "s3:ListBucketVersions",
                "s3:ListBucket",
                "lambda:CreateEventSourceMapping",
                "logs:DeleteLogStream",
                "lambda:UntagResource",
                "lambda:PutFunctionConcurrency",
                "apigateway:DELETE",
                "iam:PassRole",
                "cloudformation:DescribeStackResource*",
                "apigateway:SetWebACL",
                "iam:DeleteRolePolicy",
                "apigateway:PATCH",
                "logs:DescribeLogGroups",
                "apigateway:PUT",
                "logs:DeleteLogGroup",
                "lambda:Update*",
                "iam:ListRoles",
                "lambda:Get*",
                "cloudformation:DeleteStackSet",
                "lambda:AddPermission",
                "s3:ListAllMyBuckets",
                "cloudformation:CreateStack",
                "lambda:DeleteAlias",
                "iam:UpdateRole",
                "s3:GetBucketLocation",
                "lambda:RemovePermission",
                "cloudformation:ListChangeSets",
                "s3:GetObjectVersion"
            ],
            "Resource": "*"
        }
    ]
}
```

### 2. Project Configuration

1. In `protect.py` on lines `14-16`, configure your Organisation name, user name, and login name. For example:

```
organization = "DarkFore-t"
user_name = 'ayush_sharma'
login_name = 'ayush-sharma'
```

### 3. Deployment

1. Add your GitHubb personal access token retrieved previously to the environment by running `export GITHUB_KEY="<token>"`.
2. If you're using an AWS IAM user and not a role, use `aws configure` to configure the access key, secret, and region.
3. You can deploy the project using the following commands:

```
npm install -g serverless
npm install serverless-python-requirements
pip3 install -r requirements.txt
serverless deploy --stage prod --github-key `echo $GITHUB_KEY` --deployment-bucket <path-to-s3-bucket>
```

## Adding Branch Protection

Once deployed, Serverless will give you a API gateway URL in the output logs under `endpoints:`. Note this API gateway URL.

Go to your Github Organization settings, and go to `Settings > Webhooks > Add webhook`.
1. Enter the API Gateway URL in `Payload URL`.
2. For `Content type`, select `application/json`.
3. For `Which events would you like to trigger this webhook?`, select `Let me select individual events. `, and then select `Repositories `.
4. Hit `Add webhook`.

## Testing the project

Once the deployment is complete:

1. Create a new repo in the Organisation configured in the previous step.
2. Initialise a README.

On a successful run, your new repo should have the following changes:

1. Under `Settings > Branches > Branch protection rules`, there will be a new rule protecting the `master`.
2. A new issue will be created in this repo with the following message:

```
@ayush-sharma Branch protections were automatically added for this repo.
Protections:
{ 'required_status_checks': null, 'enforce_admins': true, 'required_pull_request_reviews': { 'dismissal_restrictions': {}, 'dismiss_stale_reviews': true, 'require_code_owner_reviews': true, 'required_approving_review_count': 2 }, 'restrictions': { 'users': [ 'ayush-sharma' ], 'teams': [ 'ayush-sharma' ] }, 'required_linear_history': true, 'allow_force_pushes': false, 'allow_deletions': false }
```
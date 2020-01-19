import json
import requests
import os


def lambda_handler(event, context):

    body = json.loads(event["body"])

    if "action" not in body or body["action"] not in ["created", "renamed"]:

        print(body)
        return ""

    organization = "DarkFore-t"
    user_name = "ayush_sharma"
    login_name = "ayush-sharma"

    repository_name = body["repository"]["name"]

    # Initial variables
    github_credentials = (user_name, os.environ.get("GITHUB_KEY", ""))
    headers = {"Accept": "application/vnd.github.luke-cage-preview+json"}
    url_branch_protection = (
        "https://api.github.com/repos/%s/%s/branches/master/protection"
        % (organization, repository_name)
    )
    url_create_issue = "https://api.github.com/repos/%s/%s/issues" % (
        organization,
        repository_name,
    )

    branch_permissions = """{
      "required_status_checks": null,
      "enforce_admins": true,
      "required_pull_request_reviews": {
        "dismissal_restrictions": {},
        "dismiss_stale_reviews": true,
        "require_code_owner_reviews": true,
        "required_approving_review_count": 2
      },
      "restrictions": {
        "users": [
          "%s"
        ],
        "teams": [
          "%s"
        ]
      },
      "required_linear_history": true,
      "allow_force_pushes": false,
      "allow_deletions": false
    }""" % (
        login_name,
        login_name,
    )

    # Add branch permissions
    response = requests.put(
        url_branch_protection,
        auth=github_credentials,
        headers=headers,
        data=branch_permissions,
    )

    if response.status_code in [200, 201]:

        print("OK")
        print(response.text)

        # Create issue with permission status
        content = """ {
                      "title": "Branch Protections added!",
                      "body": "@ayush-sharma Branch protections were automatically added for this repo.\\r\\nProtections:\\r\\n `%s`",
                      "assignees": [
                          "%s"
                       ]
                    } """ % (
            branch_permissions.replace('"', "'").replace("\n", "\\r\\n"),
            login_name,
        )

        response = requests.post(
            url_create_issue, auth=github_credentials, headers=headers, data=content
        )

        if response.status_code in [200, 201]:

            print("OK")
            print(response.text)

        else:

            print("FAIL")
            print(response.status_code)
            print(response.text)

    else:

        print("FAIL")
        print(response.status_code)
        print(response.text)

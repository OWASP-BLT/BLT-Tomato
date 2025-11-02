# BLT-Tomato
Scripts related to projects mainly for high level OWASP project management
1) Funding https://owasp-blt.github.io/BLT-Tomato/

## Features

### Slack Notifications
When new OWASP projects are added to the funding list, a notification is automatically sent to a configured Slack webhook. This helps keep the community informed about projects seeking funding.

To enable Slack notifications:
1. Create a Slack webhook URL for your workspace
2. Add it as a repository secret named `SLACK_WEBHOOK_URL`
3. The workflow will automatically send notifications when new projects are detected

If the `SLACK_WEBHOOK_URL` secret is not configured, the script will continue to work normally without sending notifications.

## Manually Triggering the Workflow

The workflow can be manually triggered using the `workflow_dispatch` event. This allows you to run the workflow on demand without waiting for a push event to the `main` branch.

To manually trigger the workflow, follow these steps:
1. Go to the "Actions" tab in your GitHub repository.
2. Select the workflow you want to run.
3. Click on the "Run workflow" button.
4. Optionally, provide any required inputs and click "Run workflow" again.

# Docker container action to run IAP Automation

## Input Parameters Required
| Parameter | Description |
| --------- | ----------- |
| IAP_INSTANCE | URL to the IAP Instance |
| IAP_TOKEN | To authenticate api requests to the instance |
| API_ENDPOINT | API endpoint name to trigger an automation |
| API_ENDPOINT_BODY | The POST body used to create the workflow input |

## Other Input Parameters (Optional)
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| JOB_STATUS | If user want to check the status of the job. (0/1) | 1 |
| TIMEOUT | Time interval to check job status (in sec) | 15 sec |
| NO_OF_ATTEMPTS | No of attempts to check job status | 10 |

## Output
| Parameter | Description |
| --------- | ----------- |
| results | API Trigger output variables |
## API
GET /health/server

POST /operations-manager/triggers/endpoint/:routeName

- ### IAP Release <= 2021.1
        GET /workflow_engine/job/:job_id/details

        GET /workflow_engine/job/:job_id/output

- ### IAP Release > 2021.1
        GET /operations-manager/jobs/:id
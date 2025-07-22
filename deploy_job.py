from databricks.sdk import WorkspaceClient
import os


server_hostname = os.getenv("DATABRICKS_HOST")
http_path = os.getenv("DATABRICKS_HTTP_PATH")
access_token = os.getenv("DATABRICKS_TOKEN")

client = WorkspaceClient(
    host=server_hostname,
    token=access_token
)



job_settings = {
    "name": "DataLoader Serverless Job",
    "environments": [
        {
            "environment_key": "default_env",
            "environment": {
                "docker_image": {
                    "url": "databricksruntime/python:latest"
                },
                "python": {
                "pip": [
                    "dbfs:/tmp/dataloader-0.1.0-py3-none-any.whl"
                ]
            }
            }
        }
    ],
    "tasks": [
        {
            "task_key": "load_data_task",
            "python_wheel_task": {
                "package_name": "dataloader",
                "entry_point": "load_data"
            },
            "environment_key": "default_env"
        }
    ]
}

created_job = client.api_client.do(
    "POST",
    "/api/2.1/jobs/create",
    body=job_settings
)

print(f"Created Job ID: {created_job['job_id']}")

with open("job_id.txt", "w") as f:
    f.write(str(created_job['job_id']))


from databricks.sdk import WorkspaceClient
import os

server_hostname = os.getenv("DATABRICKS_HOST")
access_token = os.getenv("DATABRICKS_TOKEN")

client = WorkspaceClient(
    host=server_hostname,
    token=access_token
)

job_settings = {
    "name": "DataLoader Serverless Job",
    "job_clusters": [
        {
            "job_cluster_key": "serverless_cluster",
            "new_cluster": {
                "spark_version": "14.0.x-scala2.12",
                "node_type_id": "Standard_DS3_v2",
                "num_workers": 1,
                "data_security_mode": "SINGLE_USER",
                "runtime_engine": "PHOTON"
            }
        }
    ],
    "environments": [
        {
            "environment_key": "default_env",
            "environment": {
                "docker_image": {
                    "url": "databricksruntime/python:latest"
                },
                "python": {
                    "pip": [
                        "dbfs:/FileStore/whl_poc/extract_work-0.1-py3-none-any.whl"
                    ]
                },
                "environment_version": "14.0.x-photon-scala2.12"
            }
        }
    ],
    "tasks": [
        {
            "task_key": "load_data_task",
            "job_cluster_key": "serverless_cluster",
            "python_wheel_task": {
                "package_name": "dataloader",
                "entry_point": "load_data"
            },
            "environment_key": "default_env"
        }
    ]
}

created_job = client.api_client.do(
    method="POST",
    path="/api/2.1/jobs/create",
    body=job_settings
)

print(f"Created Job ID: {created_job['job_id']}")

with open("job_id.txt", "w") as f:
    f.write(str(created_job['job_id']))
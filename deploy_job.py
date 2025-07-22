from databricks.sdk import WorkspaceClient
import os
from databricks.sdk.service.jobs import JobSettings

server_hostname = os.getenv("DATABRICKS_HOST")
http_path = os.getenv("DATABRICKS_HTTP_PATH")
access_token = os.getenv("DATABRICKS_TOKEN")

client = WorkspaceClient(
    host=server_hostname,
    token=access_token
)


job_settings = {
    "name": "DataLoader Job",
    "job_clusters": [
        {
            "job_cluster_key": "serverless_cluster",
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",  # Adjust version
                "num_workers": 1,
                "data_security_mode": "SINGLE_USER",
                "runtime_engine": "PHOTON",
                "node_type_id": "Serverless",   # This is the serverless identifier
                "custom_tags": {
                    "ClusterType": "Serverless"
                }
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
            "libraries": [
                {
                    "whl": "dbfs:/FileStore/whl_poc/extract_work-0.1-py3-none-any.whl"
                }
            ]
        }
    ]
}

# Create or update the job
created_job = client.jobs.create(**job_settings.as_dict())
print(f"Created Job ID: {created_job.job_id}")


# Save job ID to file
with open("job_id.txt", "w") as f:
    f.write(str(created_job.job_id))
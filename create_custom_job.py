import utils

from google import auth
from google.auth.transport.requests import Request

credentials, _cred_project = auth.default()
credentials.refresh(Request())
ACCESS_TOKEN = credentials.token

PROJECT_ID = "test-project"
CUSTOM_JOB_LOCATION = "us-east4"
PERSISTENT_RESOURCE_ID = "test-persistent-resource-prefix-000000000"
CUSTOM_JOB_DISPLAY_NAME = "test-custom-job-display-name"

WORKER_POOL_SPECS = [
    {
        "machine_spec": {
            "machine_type": "a2-ultragpu-1g",
            "accelerator_type": "NVIDIA_A100_80GB",
            "accelerator_count": 1,
        },
        "replica_count": 2,
        "disk_spec": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 200},
        "container_spec": {
            "image_uri": "image-repository-url",
            "command": [],
            "args": [],
        },
    }
]


def main():
    custom_job_request = {
        "display_name": CUSTOM_JOB_DISPLAY_NAME,
        "job_spec": {
            "persistent_resource_id": PERSISTENT_RESOURCE_ID,
            "worker_pool_specs": WORKER_POOL_SPECS,
        },
    }

    custom_job = utils.create_custom_job(
        custom_job=custom_job_request,
        project=PROJECT_ID,
        location=CUSTOM_JOB_LOCATION,
        access_token=ACCESS_TOKEN,
    )

    print(custom_job)


if __name__ == "__main__":
    main()

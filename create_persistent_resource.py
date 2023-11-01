import utils

import json

from google import auth
from google.auth.transport.requests import Request


### Get Credentials for API calls ###

# Can modify if you don't want to use default credentials
# Refresh credentials so that OAuth access token is added to credentials
credentials, _cred_project = auth.default()
credentials.refresh(Request())
ACCESS_TOKEN = credentials.token

### FLAGS ###

# If "TEST", will delete the cluster after confirming creation.
# Otherwise, cluster will keep running and not be deleted.
STAGE = "DEV"

### PARAMETERS ###

PROJECT_ID = "test-project"
PERSISTENT_RESOURCE_PREFIX = "test-persistent-resource-prefix"
CLUSTER_REGION = "us-east4"

# https://cloud.google.com/vertex-ai/docs/training/configure-compute
RESOURCE_POOLS = [
    {
        "machine_spec": {
            "machine_type": "a2-ultragpu-1g",
            "accelerator_type": "NVIDIA_A100_80GB",
            "accelerator_count": 1,
        },
        "replica_count": 2,
        "disk_spec": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 200},
    }
]


### DONT TOUCH! Unless you have a good understanding of the utility functions ###
# Main function does not need to be modified
if __name__ == "__main__":
    # Basic prereq assertions
    assert type(PROJECT_ID) is str, "PROJECT_ID is not defined as a string"
    assert ACCESS_TOKEN is not None, "Access token for REST API header must be present"
    assert (
        len(RESOURCE_POOLS) > 0
    ), "Must specify at least one resource pool for the persistent resource"

    # Create persistent resource
    # Add display name
    persistent_resource = utils.create_persistent_resource(
        persistent_resource_prefix=PERSISTENT_RESOURCE_PREFIX,
        resource_pools=RESOURCE_POOLS,
        project=PROJECT_ID,
        location=CLUSTER_REGION,
        access_token=ACCESS_TOKEN,
        sleep_sec=30,
    )
    print(json.dumps(persistent_resource, indent=2))

    # ONLY FOR TESTING PURPOSES! DO NOT RUN!
    # Deletes the created persistent resource
    if STAGE == "TEST":
        pr_id_to_delete = persistent_resource["displayName"]
        utils.delete_persistent_resource(
            persistent_resource_id=pr_id_to_delete,
            project=PROJECT_ID,
            location=CLUSTER_REGION,
            access_token=ACCESS_TOKEN,
        )

    # List all persistent resources in the region after the script runs
    print("Listing all persistent resources in the given project/region...")
    print(
        json.dumps(
            utils.list_persistent_resources(
                project=PROJECT_ID, location=CLUSTER_REGION, access_token=ACCESS_TOKEN
            ),
            indent=2,
        )
    )

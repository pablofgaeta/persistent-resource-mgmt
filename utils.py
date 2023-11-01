from urllib.parse import urlencode
import time
import json
from uuid import uuid4 as uuid

from typing import List

import requests


def create_custom_job(
    custom_job: dict,
    project: str,
    location: str,
    access_token: str,
):
    json_data = custom_job

    request_uri = f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{location}/customJobs"
    create_job_res = requests.post(
        request_uri,
        json=json_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    create_job = create_job_res.json()

    if create_job_res.status_code != 200:
        raise Exception(json.dumps(create_job, indent=2))

    print(f"Creating custom job: {custom_job['display_name']}")

    return create_job


def create_persistent_resource(
    persistent_resource_prefix: str,
    resource_pools: List[dict],
    project: str,
    location: str,
    access_token: str,
    sleep_sec: int,
):
    while True:
        # Create a unique id for the persistent resource for each attempt
        persistent_resource_id = f"{persistent_resource_prefix}-{str(uuid())}"
        _simple_create_persistent_resource(
            persistent_resource_id=persistent_resource_id,
            resource_pools=resource_pools,
            project=project,
            location=location,
            access_token=access_token,
        )

        # Keep checking resource state until running or error state
        while True:
            # Get persistent resource
            persistent_resource = get_persistent_resource(
                persistent_resource_id=persistent_resource_id,
                project=project,
                location=location,
                access_token=access_token,
            )
            pr_state = persistent_resource["state"]

            # Check state of resource
            if pr_state == "RUNNING":
                print("Cluster creation SUCCESSFUL.")
                return persistent_resource

            if pr_state == "ERROR":
                print("Cluster creation FAILED. Entered ERROR state")
                # Clean up failed persistent resource
                persistent_resource_to_delete = persistent_resource["displayName"]
                delete_persistent_resource(
                    persistent_resource_id=persistent_resource_to_delete,
                    project=project,
                    location=location,
                    access_token=access_token,
                )
                break

            # Sleep before next check
            time.sleep(sleep_sec)

        # Sleep before retrying creation of a new cluster
        time.sleep(sleep_sec)


def _simple_create_persistent_resource(
    persistent_resource_id: str,
    resource_pools: List[dict],
    project: str,
    location: str,
    access_token: str,
):
    json_data = {"resource_pools": resource_pools}
    id_param = urlencode({"persistent_resource_id": persistent_resource_id})

    request_uri = f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{location}/persistentResources?{id_param}"
    create_pr_res = requests.post(
        request_uri,
        json=json_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    create_pr = create_pr_res.json()

    if create_pr_res.status_code != 200:
        raise Exception(json.dumps(create_pr, indent=2))

    print(f"Creating persistent resource: {persistent_resource_id}")

    return create_pr


def list_persistent_resources(
    project: str,
    location: str,
    access_token: str,
):
    request_uri = f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{location}/persistentResources"
    list_pr_res = requests.get(
        request_uri, headers={"Authorization": f"Bearer {access_token}"}
    )
    persistent_resources = list_pr_res.json()

    if list_pr_res.status_code != 200:
        raise Exception(json.dumps(persistent_resources, indent=2))

    return persistent_resources


def get_persistent_resource(
    persistent_resource_id: str,
    project: str,
    location: str,
    access_token: str,
):
    request_uri = f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{location}/persistentResources/{persistent_resource_id}"
    check_pr_res = requests.get(
        request_uri, headers={"Authorization": f"Bearer {access_token}"}
    )
    persistent_resource = check_pr_res.json()

    if check_pr_res.status_code != 200:
        raise Exception(json.dumps(persistent_resource, indent=2))

    print(
        f"Checking persistent resource: {persistent_resource_id} (State = {persistent_resource['state']})"
    )

    return persistent_resource


def delete_persistent_resource(
    persistent_resource_id: str,
    project: str,
    location: str,
    access_token: str,
):
    request_uri = f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{location}/persistentResources/{persistent_resource_id}"
    delete_pr_res = requests.delete(
        request_uri, headers={"Authorization": f"Bearer {access_token}"}
    )
    delete_pr = delete_pr_res.json()

    if delete_pr_res.status_code != 200:
        raise Exception(json.dumps(delete_pr, indent=2))

    print(
        f"Deleting persistent resource: {persistent_resource_id} (Done = {delete_pr['done']})"
    )

    return delete_pr

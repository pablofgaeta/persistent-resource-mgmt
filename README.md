# persistent-resource-mgmt

This repository provides a simple method to virtually guarantee persistent resource cluster creation. This is useful when attempting to "reserve" very high-demand resources (e.g. A100 80GB GPUs). Requesting a cluster can occasionally result in failure and it is hard to determine when resources will be available to successfully provision the cluster.

The `create_persistent_resource.py` script will continuously request a persistent resource cluster until one has successfully been provisioned. Any intermediary attempts are automatically cleaned up.

Once the cluster has been created, users can submit Vertex Custom Jobs that run on this cluster, meaning guaranteed resource availability without the headache of cluster management. An example custom job configuration is included in the `create_custom_job.py` script.

## Getting started

```bash
# Enter working directory
cd persistent-resource-mgmt

# Create virtual environment and install dependencies... Tested in python 3.9 using virtualenv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Before calling script, configure parameters in create_persistent_resource.py

# Call create_persistent_resource file to repeatedly attempt to create a persistent resource
python create_persistent_resource.py

# Call create_custom_job to create a Vertex custom job with a specified persistent resource
```

## Files

`create_persistent_resource.py`:

- Main file for generating creating persistent resource with retries on error
- Parameters for the persistent resource should be configured in this file
- The main running code doesn't need to be modified
- See more information [here](https://cloud.google.com/vertex-ai/docs/training/persistent-resource-overview)

`utils.py`:

- Utility function file for custom job creation and CRUD operations on persistent resources. Includes both simple and smart (retries) creation for a persistent resource

`create_custom_job.py`:

- Once a persistent resource cluster has been created, this file provides an example of how to run a Custom Job with this cluster. See more information [here](https://cloud.google.com/vertex-ai/docs/training/persistent-resource-train)

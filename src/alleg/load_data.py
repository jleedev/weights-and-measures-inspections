import json
from pathlib import Path
import shutil

from ckanapi import RemoteCKAN
import requests

from .config import CONFIG

raw = Path(CONFIG["download-directory"])
raw.mkdir(exist_ok=True)

def refresh_dataset():
    dataset_id = CONFIG["dataset-id"]
    dataset_path = (raw / dataset_id).with_suffix('.json')
    ckan = RemoteCKAN(CONFIG["ckan-address"])
    dataset = ckan.action.package_show(id=dataset_id)
    with dataset_path.open('w') as w:
        json.dump(dataset, w)

    for resource in dataset['resources']:
        data_path = raw / resource['revision_id']
        if data_path.exists():
            print('[ok]', resource['name'])
            continue
        with (
            requests.get(resource['url'], stream=True) as r,
            data_path.open("wb") as w,
        ):
            r.raise_for_status()
            print(resource['name'])
            shutil.copyfileobj(
                r.raw,
                w,
            )

def get_resources():
    dataset_id = CONFIG["dataset-id"]
    dataset_path = (raw / dataset_id).with_suffix('.json')
    dataset = json.load(dataset_path.open())
    resources = {}
    for resource in dataset["resources"]:
        resources[resource["name"]] = raw / resource["revision_id"]
    return resources

if __name__ == '__main__':
    refresh_dataset()

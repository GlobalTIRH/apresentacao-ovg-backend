import time
from flask import json
import requests
from dotenv import load_dotenv
import os as osBib


load_dotenv()

def gerar_json(area_interesse):
    headers = {
        "Authorization": f"Bearer {osBib.getenv('BRIGHTDATA_API_KEY')}",
        "Content-Type": "application/json",
    }

    url = "https://api.brightdata.com/datasets/v3/trigger"
 
    params = {
        "dataset_id": "gd_lpfll7v5hcqtkxl6l",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
        "limit_per_input": "5",
    }
    area_interesse = area_interesse.lower().replace("-", " ")

    data = {
	    "input": [{"location":"Goiânia","keyword":f"{area_interesse}","time_range":"Past month","experience_level":"Internship","country":"BR","job_type":"","remote":"","company":"","location_radius":""}],
	    "custom_output_fields": ["job_title","company_name","job_location","url","job_summary"],
    }

    response = requests.post(url, headers=headers, params=params, json=data)
    response_json = response.json()

    snapshot_id = response_json.get("snapshot_id")
    get_snapshot_infos = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
    response = requests.get(get_snapshot_infos, headers=headers)

    while 'Snapshot is not ready yet, try again in 30s' in response.text:
        time.sleep(5)
        response = requests.get(get_snapshot_infos, headers=headers)

    data = response.text

    if 'Snapshot is empty' in response.text:
        return None
    
    
    data = data.replace("}", "},")
    data = "[" + data[:-1] + "]"
    data = data.replace("},]", "}]")

    job_listings = []
    for item in json.loads(data):
        description = item.get("job_summary", "")
        description = description.replace("Show more", "")
        description = description.replace("Show less", "")

        job_listings.append(
            {
                "title": item.get("job_title"),
                "company": item.get("company_name"),
                "location": item.get("job_location"),
                "description": item.get("job_summary"),
                "url": item.get("url"),
            }
        )

    
    dataset_folder = 'dataset'
    if not osBib.path.exists(dataset_folder):
        osBib.makedirs(dataset_folder)
    area_interesse = area_interesse.replace(" ", "_")
    json_file_path = osBib.path.join(dataset_folder, f'{area_interesse}_job_listings.json')
   
    with open(json_file_path, 'w') as json_file:
        json.dump(job_listings, json_file, indent=4, ensure_ascii=False)

    return job_listings

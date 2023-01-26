#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests


def save_img_to_local(url: str) -> str or bool:
    directory = f"data/images"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Splite url to str file
    filename = url.split("/")
    name = f"{directory}/{filename.pop()}"

    # Define HTTP Headers
    headers = {
        "User-Agent": "Chrome/51.0.2704.103",
    }

    # Send GET request
    response = requests.get(url, headers=headers)

    # Save the image
    if response.ok:
        with open(name, "wb") as f:
            f.write(response.content)
        return name
    else:
        print(response.status_code)
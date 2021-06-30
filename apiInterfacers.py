import os
import requests

from helperFunctions import hashFile


def reportByHash(apikey, inputFilePath):
    # Retrieves report based on MD5 hashed value of input file
    hashedFile = hashFile(inputFilePath)
    url = 'https://api.metadefender.com/v4/hash/' + hashedFile
    headers = {
        'apikey': apikey
    }
    try:
        response = requests.get(url, headers=headers)
        # Raises exception for HTTP errors, except for 404
        # 404 error should proceed to upload file instead of raising an exception and exiting
        if response.status_code != 404:
            response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response


def reportByDomain(apikey, domain):
    # Retrieves report based on a domain
    # Mostly used for experimental purposes and not necessary for main functionality
    url = 'https://api.metadefender.com/v4/domain/' + domain
    headers = {
        'apikey': apikey
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response


def reportByFile(apikey, path):
    filename = os.path.basename(path)
    # Begins report process by uploading file and returning response containing data_id for file
    url = 'https://api.metadefender.com/v4/file'
    data = open(path, 'rb').read()
    # Uploading in binary mode
    headers = {
        'apikey': apikey,
        'filename': filename,
        'Content-Type': 'application/octet-stream',
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response


def pollByDataID(apikey, dataID):
    # Retrieves current status of file scan
    url = 'https://api.metadefender.com/v4/file/' + dataID
    headers = {
        'apikey': apikey
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response

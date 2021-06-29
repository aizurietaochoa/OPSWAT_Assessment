import requests
import hashlib
import json


def fetchFile(path):
    file = open(path, 'r')
    content = file.read()
    file.close()
    return content


def reportByHash(apikey, samplefile):
    # Retrieves report based on MD5 hashed value of samplefile.txt
    hashedFile = str(hashlib.md5(samplefile.encode()).hexdigest())
    url = 'https://api.metadefender.com/v4/hash/' + hashedFile
    headers = {
        'apikey': apikey
    }
    try:
        response = requests.request("GET", url, headers=headers)
        # print(response)

        # Raises exception for HTTP errors, except for 404
        # 404 error should proceed to upload file instead of exiting
        if response.status_code != 404:
            response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response


def reportByDomain(apikey, domain):
    url = 'https://api.metadefender.com/v4/domain/' + domain
    headers = {
        'apikey': apikey
    }

    try:
        response = requests.request("GET", url, headers=headers)
        # print(response)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response


def reportByFile(apikey, path):
    url = 'https://api.metadefender.com/v4/file'
    data = open(path, 'rb').read()
    headers = {
        'apikey': apikey,
        'filename': 'samplefile.txt',
        'Content-Type': 'application/octet-stream',
    }

    try:
        response = requests.request("POST", url, data=data, headers=headers)
        # print(response)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response


def pollByDataID(apikey, dataID):
    url = 'https://api.metadefender.com/v4/file/' + dataID
    headers = {
        'apikey': apikey
    }
    try:
        response = requests.request("GET", url, headers=headers)
        # print(response)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response


def main():
    # Obtain user provided apikey
    apikey = fetchFile('apikey.txt')
    # Obtain user provided samplefile.txt
    samplefile = fetchFile('samplefile.txt')

    # Send MD5 hash of file to see if reports exist
    hashReport = reportByHash(apikey, samplefile)
    # If hash already has reports
    if hashReport.status_code == 200:
        print("Hash found in db!")
        print(hashReport.text)
    # If hash has no reports
    elif hashReport.status_code == 404:
        # Upload file and retrieve dataID
        fileReport = reportByFile(apikey, 'samplefile.txt')
        fileReport_formatted = json.loads(
            fileReport.content.decode('utf-8-sig').encode('utf-8'))
        dataID = fileReport_formatted['data_id']

        while(True):
            pollReport = pollByDataID(apikey, dataID)
            pollReport_formatted = json.loads(
                pollReport.content.decode('utf-8-sig').encode('utf-8'))
            progress = pollReport_formatted['scan_results']['progress_percentage']
            print("Polling...progress at " + progress + "%")
            if progress == 100:
                break
        print(pollReport.text)


main()

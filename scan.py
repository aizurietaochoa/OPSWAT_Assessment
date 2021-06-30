import sys
import os
import requests
import hashlib
import json


def fetchKey():
    file = open('./apikey/apikey.txt', 'r')
    apikey = file.read()
    file.close()
    return apikey


def hashFile(inputFilePath):
    # Hashes file in chunks if too large to be handled in memory
    with open(inputFilePath, "rb") as inputFile:
        file_hash = hashlib.md5()
        while chunk := inputFile.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


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


def generateReport(response):
    # Generates report according to provided guidelines
    # Requires JSON parsed response
    outputFile = open('report.txt', 'w')
    print("filename: " + str(response['file_info']['display_name']))
    print("filename: " +
          str(response['file_info']['display_name']), file=outputFile)

    print("overall_status: Clean" if response['scan_results']['scan_all_result_a']
          == "No Threat Detected" else "overall_status: Threats Detected")
    print("overall_status: Clean" if response['scan_results']['scan_all_result_a']
          == "No Threat Detected" else "overall_status: Threats Detected", file=outputFile)

    scanReports = response['scan_results']['scan_details']
    for engine in scanReports:
        print("engine: " + str(engine))
        print("engine: " + str(engine), file=outputFile)

        print("threat_found: Clean" if scanReports[engine]['threat_found'] ==
              '' else "threat_found: " + str(scanReports[engine]['threat_found']))
        print("threat_found: Clean" if scanReports[engine]['threat_found'] ==
              '' else "threat_found: " + str(scanReports[engine]['threat_found']), file=outputFile)

        print("scan_result: " + str(scanReports[engine]['scan_result_i']))
        print("scan_result: " +
              str(scanReports[engine]['scan_result_i']), file=outputFile)

        print("def_time: " + str(scanReports[engine]['def_time']))
        print("def_time: " +
              str(scanReports[engine]['def_time']), file=outputFile)

    print("END")
    print("END", file=outputFile)
    outputFile.close()
    return


def main():
    # Obtain user provided apikey
    apikey = fetchKey()
    # User provided file to be scanned
    inputFilePath = str(sys.argv[1])

    # Send MD5 hash of file to see if reports exist
    hashReport = reportByHash(apikey, inputFilePath)
    # If hash already has reports
    if hashReport.status_code == 200:
        hashReport_formatted = json.loads(
            hashReport.content.decode('utf-8-sig').encode('utf-8'))
        # Generate report based on hash request
        generateReport(hashReport_formatted)
    # If hash has no reports
    elif hashReport.status_code == 404:
        # Upload file and retrieve dataID
        fileReport = reportByFile(apikey, inputFilePath)
        fileReport_formatted = json.loads(
            fileReport.content.decode('utf-8-sig').encode('utf-8'))
        dataID = fileReport_formatted['data_id']
        # Poll until scan progress is complete
        while(True):
            pollReport = pollByDataID(apikey, dataID)
            pollReport_formatted = json.loads(
                pollReport.content.decode('utf-8-sig').encode('utf-8'))
            progress = pollReport_formatted['scan_results']['progress_percentage']
            print("Polling...progress at " + str(progress) + "%")
            # Progress at 100%
            if progress == 100:
                break
        pollReport_formatted = json.loads(
            pollReport.content.decode('utf-8-sig').encode('utf-8'))
        print("\n\n\n")
        # Generate report based on file after polling is complete
        generateReport(pollReport_formatted)


main()

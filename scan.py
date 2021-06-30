import sys
import json

from apiInterfacers import reportByHash, reportByFile, pollByDataID
from helperFunctions import fetchKey, generateReport


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


if __name__ == "__main__":
    main()

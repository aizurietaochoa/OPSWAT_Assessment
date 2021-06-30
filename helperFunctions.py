import hashlib


def fetchKey():
    # Fetches apikey from api.txt inside apikey folder in project directory
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

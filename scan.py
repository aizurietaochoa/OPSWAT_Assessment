import requests
import hashlib


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

    response = requests.request("GET", url, headers=headers)
    return response.text


def reportByDomain(apikey, domain):
    url = 'https://api.metadefender.com/v4/domain/' + domain
    headers = {
        'apikey': apikey
    }

    response = requests.request("GET", url, headers=headers)
    return response.text


def reportByFile(apikey, path):
    url = 'https://api.metadefender.com/v4/file'

    data = open(path, 'rb').read()

    headers = {
        'apikey': apikey,
        'filename': 'samplefile.txt',
        'Content-Type': 'application/octet-stream',

    }

    response = requests.request("POST", url, data=data, headers=headers)
    return response.text


def main():
    # Obtain user provided apikey
    apikey = fetchFile('apikey.txt')
    # Obtain user provided samplefile.txt
    samplefile = fetchFile('samplefile.txt')

    # hashReport = reportByHash(apikey, samplefile)
    # print(hashReport)
    # domainReport = reportByDomain(apikey, 'google.com')
    # print(domainReport)
    fileReport = reportByFile(apikey, 'samplefile.txt')
    print(fileReport)


main()

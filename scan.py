import requests
import hashlib


def fetchFile(path):
    file = open(path,'r')
    content = file.read()
    file.close()
    return content

def reportByHash(apikey, samplefile):
    # Retrieves report based on hashed value of samplefile.txt
    hashedFile = str(hashlib.md5(samplefile.encode()).hexdigest())
    url = 'https://api.metadefender.com/v4/hash/' + hashedFile
    headers = {
        'apikey': apikey
    }

    response = requests.request("GET", url, headers=headers)
    return response.text

def main():
    # Obtain user provided apikey
    apikey = fetchFile('apikey.txt')
    # Obtain user provided samplefile.txt
    samplefile = fetchFile('samplefile.txt')

    hashReport = reportByHash(apikey, samplefile)
    print(hashReport)


main()
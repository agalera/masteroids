import urllib2
import hashlib
import os
import json
download_base = "http://unkworld.com/masteroids/"
#obtain find images/* -exec md5sum {} +
j = urllib2.urlopen(download_base +'update.json')
j_obj = json.load(j)
list_download = j_obj['files']

print "create dir"
try:
    os.makedirs('masteroids')
except:
    pass
def download_file(url):

    file_name = url.split('/')[-1]
    for x in range(len(url.split('/'))-1):
        temp = ""
        if (os.path.exists('masteroids/'+url.split('/')[x]) == False):
            temp += url.split('/')[x]
        if temp != "":
            print "create dir"
            os.makedirs('masteroids/'+temp)

    u = urllib2.urlopen(download_base + url)
    f = open(str('masteroids/'+ url), 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size),

    file_size_dl = 0
    block_sz = 8192
    md5 = hashlib.md5()
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        md5.update(buffer)
        status = r"[%3.2f%%]" % (file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    return md5.hexdigest()

def md5_for_file(url_file):
    md5 = hashlib.md5()
    with open(str(url_file),'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.hexdigest()

for actual_download in list_download:
    try:
        tmp_md5 = md5_for_file('masteroids/'+actual_download['url'])
    except:
        tmp_md5 = "patatitas"
    if actual_download['md5'] != tmp_md5:
        while True:
            if actual_download['md5'] == download_file(actual_download['url']):
                actual_download['value'] = True
                break
            else:
            	print "error download, try again"

        print "\n"
    else:
        print "md5 ok"

os.system('cd masteroids & start.exe 89.141.8.30 8003')
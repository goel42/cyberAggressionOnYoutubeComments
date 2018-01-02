import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen, URLError

list_IDs = []

def fetch_part(videoID, pageToken=None):
    if (not pageToken):
        data = urlencode({'videoID': videoID}).encode("utf-8")
    else:
        data = urlencode({'videoID': videoID, 'pageToken': pageToken}).encode("utf-8")
    request = Request('http://localhost:49161/api', data=data)
    method = 'POST'
    request.get_method = lambda: method
    response = urlopen(request)
    str_response = response.read().decode('utf-8')
    info = json.loads(str_response)
    print(info)
    comments = info['comments']
    print(comments)
    # with open('woho2.json', 'a+') as outfile:  
    #     json.dump(info, outfile, indent =4)
    num_comments = info['videoCommentCount']
    video_title = info['videoTitle']
    video_thumbnail = info['videoThumbnail']
    if ("nextPageToken" in info):
        nextToken = info['nextPageToken']
    else:
        nextToken = None
    return video_title, video_thumbnail, num_comments ,comments, nextToken

def fetch_complete(videoID):
    all_comments = []

    video_title, video_thumbnail,num_comments, comments, nT = fetch_part(videoID)
    all_comments.extend(comments)

    while (nT):
        comments, nT = fetch_part(videoID, nT)
        all_comments.extend(comments)

    output = {'videoTitle': video_title, "videoThumbnail": video_thumbnail, 'videoCommentCount': num_comments, 'comments': all_comments}

    writeToFile(videoID, output)

def writeToFile (videoID, all_comments):
    filename = videoID + '.json'
    # fl = open(filename, 'a+')
    # fl.write(all_comments)
    with open(filename, 'w+') as outfile:  
        json.dump(all_comments, outfile, indent =4)

fetch_complete('-4aQFqAbHRY')
# dZ0fwJojhrs


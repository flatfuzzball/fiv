# fiv v1
# https://flatfuzzball.github.io/projects/fiv.html

import requests
import json
import mpv

# Configure MPV player
player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True, ytdl=True)

# Colors used for text
class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Invidious instance URL. Changing this to a faster one closer to you is recommended.
url = "https://iv.nboeck.de"

# Code for displaying the video page
def vidpage(id):
    rq = ''.join([url + "/api/v1/videos/", id])
    rq = requests.get(rq)
    jsn = json.loads(rq.text)
    key = 0
    print("----------")
    print(colors.HEADER + jsn["author"], "-", jsn["subCountText"], "subscribers")
    print(colors.GREEN + jsn["title"], colors.BLUE)
    print(jsn["likeCount"], "likes", colors.ENDC)
    print(jsn["lengthSeconds"], "seconds", "-", jsn["viewCount"], "views", "-", jsn["publishedText"])
    print(colors.YELLOW + "Description:", colors.ENDC)
    print(jsn["description"])
    print("----------")
    print(colors.BOLD + colors.BLUE + "[1]", colors.ENDC + "Watch")
    print(colors.BOLD + colors.BLUE + "[2]", colors.ENDC + "Comments")

    cmd = input("> ")
    if cmd == "1":

        # Play video
        vid = ''.join([url + "/watch?v=", jsn["videoId"]])
        print(colors.GREEN + "Loading video...")
        player.play(vid)
        player.wait_for_playback()
    elif cmd == "2":
        
        # Code for displaying comments
        rq = ''.join([url + "/api/v1/comments/", id])
        rq = requests.get(rq)
        jsn = json.loads(rq.text)
        print(colors.YELLOW)
        print(jsn["commentCount"], "Comments:", colors.ENDC)
        for i in jsn["comments"]:
            print("----------")
            if i["isPinned"] is True:
                print(colors.BOLD + "(pinned)")
            if i["authorIsChannelOwner"] is True:
                print(colors.BLUE + colors.BOLD + i["author"], "-", i["publishedText"], colors.ENDC)
            else:
                print(colors.HEADER + i["author"], "-", i["publishedText"], colors.ENDC)
            print(i["content"], colors.YELLOW)
            if "replies" in i:
                print(i["likeCount"], "likes", "-", i["replies"]["replyCount"], "replies", colors.ENDC)
            else:
                print(i["likeCount"], "likes", "-", "0 replies", colors.ENDC)
            if i["isEdited"] is True:
                print(colors.BOLD + "(edited)")
            print("----------")

# Code for displaying channel page
def chpage(id):
    rq = ''.join([url + "/api/v1/channels/", id])
    rq = requests.get(rq)
    jsn = json.loads(rq.text)
    print("----------")
    print(colors.HEADER + jsn["author"])
    if jsn["authorVerified"] is True:
        print(colors.BOLD + colors.BLUE + "☑", colors.ENDC, colors.YELLOW)
    print(jsn["subCount"], "subscribers", "-", jsn["totalViews"], "total views", colors.ENDC)
    print(jsn["description"])
    print(colors.YELLOW + "Latest videos:", colors.ENDC)
    key = 0
    for i in jsn["latestVideos"]:
        if key == 6:
            break
        else:
            print("----------", colors.BOLD)
            print(key, colors.ENDC)
            print(colors.GREEN + i["title"], colors.ENDC)
            print(i["lengthSeconds"], "seconds", "-", i["viewCountText"], "-", i["publishedText"])
            print("----------")   
            key += 1
    print(colors.BOLD + colors.BLUE + "[6]", colors.ENDC + "All videos")
    
    key = 0

    view = int(input("> "))
    if view <= 5:

        # Open selected video
        vidpage(jsn["latestVideos"][view]["videoId"])
    elif view == 6:
        
        # Display all (top like 59 cause of API) videos
        rq = ''.join([url + "/api/v1/channels/", id, "/videos"])
        rq = requests.get(rq)
        jsn = json.loads(rq.text)
        for i in jsn["videos"]:
            print("----------", colors.BOLD)
            print(key, colors.GREEN)
            print(i["title"], colors.ENDC)
            print(i["lengthSeconds"], "seconds", "-", i["viewCountText"], "-", i["publishedText"])
            print("----------")
            key += 1
        view = int(input("> "))
        vidpage(jsn["videos"][view]["videoId"])

# "Main menu", start of program
rq = requests.get(url + "/api/v1/stats")
jsn = json.loads(rq.text)

print(colors.RED + jsn["software"]["name"])
print("Running version:", jsn["software"]["version"])
print("Total users:", jsn["usage"]["users"]["total"], colors.ENDC)

print(colors.BOLD + colors.BLUE + '''
[1]''' + colors.ENDC, "Trending")
print(colors.BOLD + colors.BLUE + "[2]" + colors.ENDC, "Search")

cmd = input("> ")

if cmd == "1":
    # Show trending page
    key = 0
    rq = requests.get(url + "/api/v1/trending")
    jsn = json.loads(rq.text)
    for i in jsn:
        print("----------", colors.BOLD)
        print(key)
        print(colors.ENDC + colors.HEADER + i["author"], colors.ENDC)
        if i["liveNow"] == True:
            print(colors.RED + colors.BOLD + "LIVE!", colors.ENDC)
        print(colors.GREEN + i["title"], colors.ENDC)
        print(i["lengthSeconds"], "seconds", "-", i["viewCountText"], "-", i["publishedText"])
        print("----------")
        key += 1
    
    view = int(input("> "))
    vidpage(jsn[view]["videoId"])

if cmd == "2":
    # Search for videos/channels
    key = 0
    query = input("search: ")
    rq = requests.get(url + "/api/v1/search?q=" + query)
    jsn = json.loads(rq.text)
    for i in jsn:
        print("----------", colors.BOLD)
        print(key)
        print(colors.ENDC + colors.RED + i["type"])
        # Difference between video/channel/playlist
        if i["type"] == "video" or i["type"] == "playlist":
            print(colors.HEADER + i["author"])
            print(colors.GREEN + i["title"], colors.ENDC)
            if i["type"] == "video":
                print(i["lengthSeconds"], "seconds", "-", i["viewCount"], "views", "-", i["publishedText"])
        else:
            print(colors.HEADER + i["author"], colors.BLUE)
            print(i["subCount"], "subscribers", "-", i["videoCount"], "videos", colors.ENDC)
        print("----------")
        key += 1
    
    view = int(input("> "))
    if jsn[view]["type"] == "video":
        vidpage(jsn[view]["videoId"])
    elif jsn[view]["type"] == "channel":
        chpage(jsn[view]["authorId"])
    else:
        # No playlist code in place
        print(colors.RED + "Not supported yet!")

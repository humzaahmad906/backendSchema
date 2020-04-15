import json
import cv2
import numpy as np
import asyncio
import websockets
import base64
async def hello(websocket, path):
    countf = 0
    countb = 0
    array = np.zeros((1000, 2), dtype = np.uint16)
    array1 = np.zeros((1000, 2), dtype = np.uint16)
    while True:
        name = await websocket.recv()
        name1 = json.loads(name)
        print(name1)
        img = 0
        if name1['event'] == 'image':
            imgdata = str(name1['data'])[22:]
            #print(imgdata)
            img = base64.b64decode(imgdata)
            with open('img.jpg', 'wb') as f:
                f.write(img)

            img = cv2.imread('img.jpg')
        elif name1['event'] != 'register' and name1['event'] != 'image':
            
            if name1["event"] == 'b':
                if "x" in name1["data"].keys():
                    array[countb, 0] = name1["data"]["x"]
                if "y" in name1["data"].keys():
                    array[countb, 1] = name1["data"]["y"]
                countb = countb + 1
            if name1["event"] == 'f':
                if "x" in name1["data"].keys():
                    array1[countf, 0] = name1["data"]["x"]
                if "y" in name1["data"].keys():
                    array1[countf, 1] = name1["data"]["y"]
                countf = countf + 1

        else:

            if array[0, 0] != 0 and array1[0, 0] != 0 and array[0, 1] != 0 and array1[0, 1] != 0:
                foreClicks = array1[np.random.permutation(countf)[:2]]
                backClicks = array[np.random.permutation(countb)[:2]]
                print(foreClicks)
                print(backClicks)


                image = cv2.imread('img.jpg')
                mask = np.zeros(image.shape[0:2])
                for i in range(image.shape[0]):
                    for j in range(image.shape[1]):
                        if image[i, j, 1] > 100:
                            mask[i, j] = 255
                _, frame = cv2.imencode('.JPEG', mask)
                frame = str(base64.b64encode(frame))
                mask.flatten()
                mask = mask.tolist()

                dit = {"array": frame}
                y = json.dumps({"event": "IMAGE SENT",
                                "data": {
                                    "img": dit
                                }})
                await websocket.send(y)


start_server = websockets.serve(hello, "192.168.100.120", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
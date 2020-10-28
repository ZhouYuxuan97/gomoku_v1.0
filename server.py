import asyncio
import json
import websockets
import numpy as np

# name:websockets
USERS = {}
peopleList = []
colorList = ["black", "white"]
HORIZONTAL_SIZE = 20
VERTICAL_SIZE = 20
turn = 'black'
# level 0: black, level 1: white
checkerBoard3D = np.zeros((VERTICAL_SIZE, HORIZONTAL_SIZE, 2))
checkerBoard = []


async def chat(websocket, path):
    global VERTICAL_SIZE, HORIZONTAL_SIZE
    # shakehand
    await websocket.send(json.dumps({"type": "handshake"}))
    async for message in websocket:
        data = json.loads(message)
        print(data)
        message = ''
        # send message
        if data["type"] == 'send':
            name = '404'
            for k, v in USERS.items():
                if v == websocket:
                    name = k
            if len(USERS) != 0:  # asyncio.wait doesn't accept an empty list
                message = json.dumps(
                    {"type": "user", "content": data["content"], "from": name})
        # login
        elif data["type"] == 'login':
            # people = {}
            # people["name"] = data["content"]
            # people["websocket"] = websocket
            if (len(colorList) == 0):
                color = "visitor"
            else:
                color = colorList.pop()
            # peopleList.append(people)
            USERS[data["content"]] = websocket
            if len(USERS) != 0:  # asyncio.wait doesn't accept an empty list
                if (len(colorList) == 0 and color !='visitor') :
                    message = json.dumps(
                        {"type": "init", "content": data["content"], "color": color, "HORIZONTAL_SIZE": HORIZONTAL_SIZE,
                         "VERTICAL_SIZE": VERTICAL_SIZE, "user_list": list(USERS.keys())})
                    print(message)
                else:
                    message = json.dumps(
                        {"type": "login", "content": data["content"], "color": color, "user_list": list(USERS.keys())})
                    print(message)

        # user exit
        elif data["type"] == 'logout':
            del USERS[data["content"]]
            if (data["color"] != 'visitor'):
                colorList.append(data['color'])
            if len(USERS) != 0:  # asyncio.wait doesn't accept an empty list
                message = json.dumps(
                    {"type": "logout", "content": data["content"], "color": data['color'],
                     "user_list": list(USERS.keys())})
                print(message)

        # user put chess
        elif data["type"] == 'put':
            if checkGameover(data["x"], data["y"], data["color"]):
                message = json.dumps(
                    {"type": "gameover", "color": data["color"], "x": data["x"], "y": data["y"]})
            else:
                if (data["color"] == "white"):
                    checkerBoard3D[data["x"]][data["y"]][1] = 1
                else:
                    checkerBoard3D[data["x"]][data["y"]][0] = 1
                message = json.dumps(
                    {"type": "put", "color": data["color"], "x": data["x"], "y": data["y"]})
        # set checkerboard
        elif data["type"] == 'set':

            VERTICAL_SIZE = int(data['ver'])
            HORIZONTAL_SIZE = int(data['hor'])
            checkerBoard3D = np.zeros((VERTICAL_SIZE, HORIZONTAL_SIZE, 2))
        # broadcast
        await asyncio.wait([user.send(message) for user in USERS.values()])


def checkGameover(x, y, color):
    if (checkAllDirections(color, x, y, 1, 1) or checkAllDirections(color, x, y, 0, 1) or checkAllDirections(color, x,
                                                                                                             y, 1,
                                                                                                             0) or checkAllDirections(
            color, x, y, -1, 1)):
        return True
    else:
        return False


def checkAllDirections(color, x, y, a, b):
    # type = this.rooms[roomId].checkerBoard[x][y].type
    # tempCheckerBoard = this.rooms[roomId].checkerBoard
    if (color == 'black'):
        level = 0
    else:
        level = 1
    total = 1
    tx = x + a
    ty = y + b
    while (tx >= 0 and tx < HORIZONTAL_SIZE and ty >= 0 and ty < VERTICAL_SIZE and checkerBoard3D[tx][ty][level] == 1):
        total += 1
        tx += a
        ty += b

    tx = x - a
    ty = y - b
    while (tx >= 0 and tx < HORIZONTAL_SIZE and ty >= 0 and ty < VERTICAL_SIZE and checkerBoard3D[tx][ty][level] == 1):
        total += 1
        tx -= a
        ty -= b
    if (total == 5):
        return True
    return False


start_server = websockets.serve(chat, "127.0.0.1", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

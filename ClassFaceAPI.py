import urllib, http, json, time, sys
import classes.ClassConfig
import classes.ClassPersonGroup
class Face:
    def __init__(self) -> None:
        self.config = classes.ClassConfig.Config().readConfig()
        #用本地端的圖檔進行辨識
    def detectLocalImage(self, imagepath):
        headers = {
            "Content-Type": "application/octet-stream",
            #用本地圖檔辨識
            "Ocp-Apim-Subscription-Key": self.config["api_key"],
        }
        params = urllib.parse.urlencode(
            {
                "returnFaceId": "true",
                "returnFaceLandmarks": "false",
                "returnFaceAttributes": "age,gender",
                "returnRecognitionModel": "false",
                "detectionModel": "detection_01",
                "faceIdTimeToLive": "86400",
            }
        )
        print("imagepath=", imagepath)
        requestbody = open(imagepath, "rb").read()
        try:
            conn = http.client.HTTPSConnection(self.config["host"])
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody, headers)
            response = conn.getresponse()
            data = response.read()
            json_face_detect = json.loads(str(data, "UTF-8"))
            print("detectLocalImage.faces=", json_face_detect)
            print(parsed[0]['faceId'])
            faceids.append(parsed[0]['faceId'])
            conn.close()
            print("detectLocalImage:", f"{imagepath} 偵測到 {len(json_face_detect)} 個人")
            return json_face_detect
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
            #網路的圖檔進行辨識
    def detectImageUrl(self, imageurl):
        headers = {
            "Content-Type": "application/json",  #用網路圖檔辨識
            "Ocp-Apim-Subscription-Key": self.config["api_key"],
        }
        params = urllib.parse.urlencode(
            {
                "returnFaceId": "true",
                "returnFaceLandmarks": "false",
                "returnFaceAttributes": "age,gender",
                "returnRecognitionModel": "false",
                "detectionModel": "detection_01",
                "faceIdTimeToLive": "86400",
            }
        )
        print("imageurl=", imageurl)
        requestbody = '{"url": "' + imageurl + '"}'
        try:
            conn = http.client.HTTPSConnection(self.config["host"])
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody, headers)
            response = conn.getresponse()
            data = response.read()
            json_face_detect = json.loads(str(data, "UTF-8"))
            print("detectImageUrl.faces=", json_face_detect)
            conn.close()

            print("detectImageUrl:", f"{imageurl} 偵測到 {len(json_face_detect)} 個人")
            return json_face_detect
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
    def identify(self, faceidkeys, personGroupId):
        print("def Face.identify 開始辨識。faceidkeys=", faceidkeys)
        if len(faceidkeys) == 0:
            return []
        start = int(round(time.time() * 1000))
        print("開始辨識 identify 0 ms")
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.config["api_key"],
        }
        params = urllib.parse.urlencode({})
        requestbody = (
            '''{
            "personGroupId": "'''
            + personGroupId
            + """",
            "faceIds":"""
            + str(faceidkeys)
            + """,
            "maxNumOfCandidatesReturned":1,
            "confidenceThreshold": """
            + str(self.config["confidence"])
            + """
        }"""
        )
        print('requestbody=', requestbody)
        try:
            conn = http.client.HTTPSConnection(self.config['host'])
            conn.request(
                "POST", "/face/v1.0/identify?%s" % params, requestbody, headers
            )
            response = conn.getresponse()
            data = response.read()
            identifiedfaces = json.loads(str(data, "UTF-8"))
            print("Face.Identify.identifiedfaces=", identifiedfaces)
            conn.close()
            ClassUtils.tryFaceAPIError(identifyfaces)
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
            sys.exit()
        if "error" in identifiedfaces:
            print("Error: " + identifiedfaces["error"]["code"])
            if identifiedfaces['error']['code'] == 'PersonGroupNotFound':
                personGroupAPI = classes.ClassPersonGroup.PersonGroup()
                personGroupAPI.createPersonGroup(
                    personGroupId, self.config["personGroupName"], "group userdata"
                )
                return self.identify(faceidkeys, personGroupId)
        return identifiedfaces

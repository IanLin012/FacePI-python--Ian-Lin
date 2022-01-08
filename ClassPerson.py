import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import classes.ClassConfig
import classes.ClassPersonGroup

config = classes.ClassConfig.Config().readConfig()


class Person:
    def __init__(self):
        self.api_key = config["api_key"]
        self.host = config["host"]

    def add_a_person_face(self, imagepath, personId, personGroupId):
        print(
            "'add_a_person_face': 用一個圖片放入一個 person 當中 personId=" + personId,
            "imagepath=",
            imagepath,
        )

        headers = {
            "Content-Type": "application/octet-stream",  # 上傳圖檔
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        params = urllib.parse.urlencode(
            {
                # Request parameters
                "personGroupId": personGroupId,
                #'personId': '03cb1134-ad35-4b80-8bf2-3200f44eef31',
                "personId": personId,
                #'userData': '{string}',
                #'targetFace': '{string}',
            }
        )
        requestbody = open(imagepath, "rb").read()

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "POST",
                "/face/v1.0/persongroups/"
                + personGroupId
                + "/persons/"
                + personId
                + "/persistedFaces?%s" % params,
                requestbody,
                headers,
            )
            response = conn.getresponse()
            data = response.read()
            jsondata = json.loads(str(data, "UTF-8"))
            print("add_a_person_face json:")
            conn.close()

        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

        # try:
        #     if ClassUtils.isFaceAPIError(jsondata):
        #         return []
        # except MyException.RateLimitExceededError as e:
        #     time.sleep(10)
        #     return self.add_a_person_face(imagepath, personId, personGroupId)
        # except MyException.UnspecifiedError as e:
        #     return

    def create_a_person(self, personGroupId, name, userData):
        # person group 已經存在的話，這裡會出錯。
        # personGroupApi = classes.ClassPersonGroup.PersonGroup()
        # personGroupApi.createPersonGroup(
        #     config["personGroupId"], config["personGroupName"], "group userdata"
        # )

        print(
            "'create_a_person': 在 personGroupid="
            + personGroupId
            + " 裡 建立一個 person name="
            + name
        )
        headers = {
            # Request headers
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        params = urllib.parse.urlencode({"personGroupId": personGroupId})
        requestbody = '{"name":"' + name + '","userData":"' + userData + '"}'

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "POST",
                "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params,
                requestbody.encode("UTF-8"),
                headers,
            )
            response = conn.getresponse()
            data = response.read()
            create_a_person_json = json.loads(str(data, "UTF-8"))
            print(create_a_person_json)
            conn.close()
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

        if "error" in create_a_person_json:
            print("Error: " + create_a_person_json["error"]["code"])
            if create_a_person_json["error"]["code"] == "PersonGroupNotFound":
                personGroupApi = classes.ClassPersonGroup.PersonGroup()
                personGroupApi.createPersonGroup(
                    config["personGroupId"], config["personGroupName"], "group userdata"
                )
                return self.create_a_person(personGroupId, name, userData)
        # try:
        #     if ClassUtils.isFaceAPIError(create_a_person_json):
        #         return []
        # except MyException.RateLimitExceededError as e:
        #     time.sleep(10)
        #     return self.create_a_person(personGroupId, name, userData)
        # except MyException.PersonGroupNotFoundError as e:
        #     personGroupApi = PersonGroup(self.api_key, self.host)
        #     personGroupApi.createPersonGroup(
        #         config["personGroupId"], config["personGroupName"], "group userdata"
        #     )
        #     return self.create_a_person(personGroupId, name, userData)
        # except MyException.UnspecifiedError as e:
        #     return

        return create_a_person_json["personId"]

    def add_personimages(self, personGroupId, personname, userData, imagepaths):
        """# 加入一個人的一張或多張圖片，但不訓練"""
        print("personname=", personname, "圖檔:", imagepaths)
        # person = self.getPersonByName(personGroupId, personname)
        # if person == None:
        print("call create_a_person")
        personid = self.create_a_person(personGroupId, personname, userData)
        for imagepath in imagepaths:
            self.add_a_person_face(imagepath, personid, personGroupId)
        # else:
        #    print('call add_a_person_face, personId=', person['personId'])
        #    for imagepath in imagepaths:
        #        self.add_a_person_face(imagepath, person['personId'],
        #                                    personGroupId)

    def get_a_person(self, personId, personGroupId):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", "/face/v1.0/persongroups/" + personGroupId +
                         "/persons/" + personId + "?%s" % params, "{body}",
                         headers)
            response = conn.getresponse()
            data = response.read()
            personjson = json.loads(str(data, 'UTF-8'))
            conn.close()

            # try:
            #     if ClassUtils.isFaceAPIError(personjson):
            #         return None
            # except MyException.RateLimitExceededError as e:
            #     time.sleep(10)
            #     return self.get_a_person(personId, personGroupId)
            # except MyException.UnspecifiedError as e:
            #     return
            # except MyException.PersonGroupNotTrainedError as e:
            #     print('ERROR: get_a_person.PersonGroupNotTrainedError')
            #     return
            return personjson
            
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

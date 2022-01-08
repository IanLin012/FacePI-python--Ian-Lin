import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import classes.ClassConfig

config = classes.ClassConfig.Config().readConfig()


class PersonGroup:
    def __init__(self):
        self.api_key = config["api_key"]
        self.host = config["host"]

    def train_personGroup(self):
        personGroupId = config["personGroupId"]
        print(
            "train_personGroup: 開始訓練一個 personGroup personGroupId=" + personGroupId + "。"
        )

        headers = {
            # Request headers
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        # params = urllib.parse.urlencode({"personGroupId": personGroupId})
        params = urllib.parse.urlencode({})
        body = ""
        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "POST",
                "/face/v1.0/persongroups/" + personGroupId + "/train?%s" % params,
                f"{body}",
                headers,
            )
            response = conn.getresponse()
            data = response.read()

            print("train_personGroup:" + str(data, "UTF-8"))
            conn.close()
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

    def createPersonGroup(self, personGroupId, groupname, groupdata):
        print("createPersonGroup: 建立一個 personGroupid = " + personGroupId)
        headers = {
            # Request headers.
            "Content-Type": "application/json",
            # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        # Replace 'examplegroupid' with an ID you haven't used for creating a group before.
        # The valid characters for the ID include numbers, English letters in lower case, '-' and '_'.
        # The maximum length of the ID is 64.
        # personGroupId = 'examplegroupid'
        # personGroupId = 'jiangsir_groupid2'

        # The userData field is optional. The size limit for it is 16KB.
        # personGroupId = personGroupId.encode(encoding='utf-8')
        # params = urllib.parse.urlencode(personGroupId)
        body = "{ 'name':'" + groupname + "', 'userData':'" + groupdata + "' }"

        try:
            # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
            #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
            #   URL below with "westus".
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "PUT",
                "/face/v1.0/persongroups/{}".format(personGroupId),
                body.encode(encoding="utf-8"),
                headers,
            )
            print("=============")
            response = conn.getresponse()
            data = response.read()
            jsondata = json.loads(str(data, "UTF-8"))
            print(jsondata)

            # 'OK' indicates success. 'Conflict' means a group with this ID already exists.
            # If you get 'Conflict', change the value of personGroupId above and try again.
            # If you get 'Access Denied', verify the validity of the subscription key above and try again.
            print(response.reason)
            conn.close()
            self.train_personGroup()
            return personGroupId
        except Exception as e:
            print(e.args)

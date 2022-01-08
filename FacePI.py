import fire, os, json, time
import http.client, urllib.request, urllib.parse, urllib.error, base64
import classes.ClassOpenCV
import classes.ClassFaceAPI
import classes.ClassPerson
import classes.ClassPersonGroup
import classes.ClassConfig

config = classes.ClassConfig.Config().readConfig()


class FacePI:
    def show_opencv(self):
        classes.ClassOpenCV.show_opencv("")

    def Identify(self, pictureurl):
        """14: 進行「辨識」，使用 image URL or 檔案路徑"""
        start = int(round(time.time() * 1000))
        print("開始計時 identify")
        faceApi = classes.ClassFaceAPI.Face()
        personApi = classes.ClassPerson.Person()
        print("載入 class", int(round(time.time() * 1000) - start), "ms")
        # imageurl = input('請輸入準備要辨識的 image URL or 檔案路徑:')
        if pictureurl.startswith("http"):
            detectfaces = faceApi.detectURLImages(pictureurl)
        else:
            pictureurl = pictureurl.strip()
            # statinfo = os.stat(pictureurl)
            # print("檔案大小：", statinfo.st_size, "Bytes")
            # if statinfo.st_size < 1024:
            #     print("圖檔太小 不可小於 1KB")
            #     sys.exit(1)
            # elif statinfo.st_size > 4 * 1024 * 1024:
            #     print("圖檔太大 不可大於 4MB")
            #     im = Image.open(pictureurl)
            #     out = im.resize((128, 128))
            #     im.save(pictureurl, "JPEG")
            #     print("out=", type(out))
            detectfaces = faceApi.detectLocalImage(pictureurl)

        # if len(detectfaces) == 0:
        #     print('相片中找不到人！')
        #     sys.exit(1)

        faceids = []
        for detectface in detectfaces:
            print("所偵測到的 faceId=", detectface["faceId"])
            faceids.append(detectface["faceId"])

        print("Identify.detectfaces=", detectfaces)

        #        try:
        identifiedfaces = faceApi.identify(faceids[:10], config["personGroupId"])
        # print("在所提供的相片中偵測到 identifyfaces 共 ", len(identifiedfaces), "個")
        # except MyException.PersonGroupNotTrainedError as e:
        #     print("接到例外！MyException.PersonGroupNotTrainedError as e")
        #     print("Identify.detectedFaces=", detectfaces)
        #     ClassCV.cv_Identifyfaces(detectfaces, pictureurl)
        #     # ClassTK.tk_UnknownPerson('texttest....', pictureurl, pictureurl)

        #     return
        print("在所提供的相片中偵測到 identifyfaces 共 ", len(identifiedfaces), "個")

        # successes = []
        for identifiedface in identifiedfaces:
            for candidate in identifiedface["candidates"]:
                personId = candidate["personId"]
                person = personApi.get_a_person(personId, config["personGroupId"])
                identifiedface["person"] = person
                identifiedface["confidence"] = candidate["confidence"]
                identifiedface["personId"] = candidate["personId"]

        ### cv_Identifyfaces() 精簡版
        for identifyface in identifiedfaces:
            if "person" not in identifyface:
                print("identifyface=", identifyface)
                print("無法辨識此人，請先訓練!!")
            else:
                name = identifyface["person"]["name"]
                confidence = float(identifyface["confidence"])
                if confidence >= 0.9:
                    print(name + " 簽到成功!!!")
                elif confidence >= 0.8:
                    print(name + " 簽到成功!!")
                elif confidence >= 0.7:
                    print(name + " 簽到成功!")
                else:
                    print(name + " 簽到成功")

    def Signin(self):
        """
        刷臉簽到
        """
        #        imagepath = '202994853.jpg'
        #        imagepath = 'face4.jpg'
        #        self.detectLocalImage(imagepath)
        #
        # imageurl = 'https://cdn-news.readmoo.com/wp-content/uploads/2016/07/Albert_einstein_by_zuzahin-d5pcbug-1140x600.jpg'
        # imageurl = 'https://cdn2.momjunction.com/wp-content/uploads/2020/11/facts-about-albert-einstein-for-kids-720x810.jpg'
        # classes.ClassFaceAPI.Face().detectImageUrl(imageurl)
        imagepath = classes.ClassOpenCV.show_opencv()
        # json_face_detect = classes.ClassFaceAPI.Face().detectLocalImage(imagepath)
        self.Identify(imagepath)

    def Train(self, userData=None, personname=None):
        """1. 用 3 連拍訓練一個新人"""
        jpgimagepaths = []
        for i in range(3):
            jpgimagepath = classes.ClassOpenCV.show_opencv(
                hint=" (訓練第 " + str(i + 1) + " 張)"
            )
            jpgimagepaths.append(jpgimagepath)

        if personname == None:
            personname = input("請輸入您的姓名: ")

        if userData == None:
            userData = input("請輸入您的說明文字(比如: 高師大附中國一仁): ")

        basepath = os.path.dirname(os.path.realpath(__file__))
        jpgtrainpaths = []
        for jpgimagepath in jpgimagepaths:
            filename = os.path.basename(jpgimagepath)
            # home = os.path.expanduser("~")
            jpgtrainpath = os.path.join(
                basepath, "traindatas", userData, personname, filename
            )
            if not os.path.exists(os.path.dirname(jpgtrainpath)):
                os.makedirs(os.path.dirname(jpgtrainpath))
            os.rename(jpgimagepath, jpgtrainpath)
            jpgtrainpaths.append(jpgtrainpath)

        myconfig = classes.ClassConfig.Config().readConfig()

        personAPI = classes.ClassPerson.Person()
        personAPI.add_personimages(
            myconfig["personGroupId"], personname, userData, jpgtrainpaths
        )
        personGroupapi = classes.ClassPersonGroup.PersonGroup()
        personGroupapi.train_personGroup()


if __name__ == "__main__":
    fire.Fire(FacePI)

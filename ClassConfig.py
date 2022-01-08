import json, os

class Config:
    def __init__(self) -> None:
        basepath = os.path.dirname(os.path.realpath(__file__))
        self.configpath = os.path.join(basepath, '../Config.json')

    def writeConfig(self, config):
        with open(self.configpath, 'w', encoding='utf-8') as f:
            json.dump(config, f,  ensure_ascii=False)

    def readConfig(self):
        if not os.path.exists(self.configpath):
            config = dict()
            config['api_key'] = "b9160fbd882f47bd821205a4bce64354"
            config['host'] = "eastasia.api.cognitive.microsoft.com"
            config['confidence'] = 0.6
            config['title'] = '高師大附中多元選修'
            config['personGroupName'] = '預設人群名稱'
            config['personGroupId'] = 'default_personGroupId'
            self.writeConfig(config)

        with open(self.configpath, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config


    def setConfig(self):
        config = self.readConfig()
        print('每個參數後的[]內代表目前的設定值，直接按 ENTER 代表不更改。')
        api_key = input(f'請輸入有效的 API_KEY[{config["api_key"]}]: ')
        if api_key: config['api_key'] = api_key
        title = input(f'請輸入 title[{config["title"]}]: ')
        if title: config['title'] = title

        self.writeConfig(config)
        #print(type(config))

import os
import time
from PIL import Image, ImageDraw, ImageFont, ImageTk
import cv2
import numpy as np
import classes.ClassConfig
config = classes.ClassConfig.Config().readConfig()
ttf = "C:/Windows.old/Windows/Fonts/msjhbd.ttc"
#字體 : 微軟正黑體
def getTakePicturePath(personGroupId):
    ''' 取得拍照後要存檔的路徑。 '''
    basepath = os.path.dirname(os.path.realpath(__file__))
    jpgimagepath = os.path.join(
        basepath, '../takepictures', personGroupId + "_" +
        time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".jpg")
    if not os.path.exists(os.path.dirname(jpgimagepath)):
        os.makedirs(os.path.dirname(jpgimagepath))
    return jpgimagepath
def show_opencv(hint='', mirror=True):
    ''' 顯示主畫面 '''
    cam = cv2.VideoCapture(config['videoid'])
    print('cam opening...')
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print('cam opened')
    cam.set(3, 1280)
    #修改解析度 寬
    cam.set(4, 1280 // 16 * 10)
    #修改解析度 高
    print('WIDTH', cam.get(3), 'HEIGHT', cam.get(4))
    #顯示預設的解析度
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        H, W = img.shape[:2]
        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 
        pil_im = Image.fromarray(cv2_im)
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype(ttf, 40, encoding="utf-8")
        hintfont = ImageFont.truetype(ttf, 24, encoding="utf-8")
        hints = "請按「ENTER」繼續" + hint
        w, h = draw.textsize(hints, font=hintfont)
        draw.rectangle(
            ((W / 2 - w / 2 - 5, H - h), (W / 2 + w / 2 + 5, H)), fill="red")
        hintlocation = (W / 2 - w / 2, H - h)
        textlocation = (0,0)
        draw.text(
            hintlocation, hints, (0, 255, 255),
            font=hintfont)
        cv2_text_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

        if ClassUtils.isWindows():
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)

        cv2.imshow("window", cv2_text_im)
        cv2.imshow("window", img)
        key = cv2.waitKey(1)
        if key == ord(' ') or key == 3 or key == 13:
        #space or enter
            picturepath = getTakePicturePath(
                config['personGroupId'])
            ret_val, img = cam.read()
            cv2.imwrite(picturepath, img)
            cv2.destroyAllWindows()
            cv2.VideoCapture(0).release()
            return picturepath
        elif key == 27:
        #esc to quit
            cv2.destroyAllWindows()
            cv2.VideoCapture(0).release()
            raise print("偵測到 esc 結束鏡頭")
        else:
            if key != -1:
                print('key=', key)
def show_ImageText(title, hint, facepath=None, picture=None, identifyfaces=None, personname=None):
    ''' 標準 cv 視窗'''
    import cv2
    import numpy as np
    if facepath == None:
        img = np.zeros((400, 400, 3), np.uint8)
        img.fill(90)
    else:
        img = cv2.imread(facepath)
        print('__cv_ImageText.imagepath=', facepath)
        H, W = img.shape[:2]
        img = cv2.resize(img, (400, int(H / W * 400)))
    windowname = facepath
    H, W = img.shape[:2]
    img = cv2.resize(img, (400,int(H/W*400)))
    cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #cv2和PIL中顏色的hex碼的儲存順序不同
    pil_im = Image.fromarray(cv2_im)
    draw = ImageDraw.Draw(pil_im)
    # 括號中為需要打印的canvas，這裡就是在圖片上直接打印
    titlefont = ImageFont.truetype(ttf, 24, encoding="utf-8")
    hintfont = ImageFont.truetype(ttf, 18, encoding="utf-8")
    w, h = draw.textsize(title, font=titlefont)
    draw.rectangle(
        ((W / 2 - w / 2 - 5, 0), (W / 2 + w / 2 + 5, h + 20)), fill="black")
    titlelocation = (W / 2 - w / 2, 5)
    if identifyfaces != None and len(identifyfaces) == 1:
        hint = hint + "或按 'a' 新增身份"
    w, h = draw.textsize(hint, font=hintfont)
    draw.rectangle(
        ((W / 2 - w / 2 - 5, H - h), (W / 2 + w / 2 + 5, H)), fill="red")
    hintlocation = (W / 2 - w / 2, H - h)
    draw.text(titlelocation, title, (0, 255, 255), font=titlefont)
    draw.text(hintlocation, hint, (0, 255, 0), font=hintfont)
    cv2_text_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    cv2.imshow(windowname, cv2_text_im)
    key = cv2.waitKey(10000)
    if key == ord(' ') or key == 3 or key == 13:
    #space or enter
        cv2.destroyWindow(windowname)
    elif key == ord('a') and len(identifyfaces) == 1:
        # 鍵盤 a 代表要新增 oneshot
        cv2.destroyWindow(windowname)
        ClassTK.tk_UnknownPerson('您哪位？', facepath, picture, personname)

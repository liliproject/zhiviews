import hashlib
import random
import uuid
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


# 生成验证码
def proverifycode(request):
    # 1.创建画布Image对象
    img = Image.new(mode='RGB', size=(100,30), color=(220,220,180))

    # 2. 创建画笔 ImageDraw对象
    draw = ImageDraw.Draw(img, 'RGB')

    # 3. 画文本
    # 随机产生0-9，A-Z，a-z范围的字符
    chars=''
    # font = ImageFont.truetype(font='static/fonts/hktt.ttf', size=25)
    font = ImageFont.truetype(font='static/fonts/Fangz.ttf',size=25)
    while len(chars)<4:
        flag = random.randrange(3)
        char = chr(random.randint(48,57)) if not flag else \
                chr(random.randint(65,90)) if flag==1 else \
                chr(random.randint(97, 122))
        if len(chars)==0 or chars.find(char)==-1:
            chars += char

    # 将生成的验证码的字符串存入在session
    request.session['verifycode'] = chars

    for char in chars:
        xy = (10+chars.find(char)*20, random.randrange(1,6))
        color = (random.randrange(255), random.randrange(255), random.randrange(255))
        draw.text(xy=xy,
                  text=char,
                  fill=color,
                  font= font)

    for i in range(200):
        xy=(random.randrange(120), random.randrange(30))
        color = (random.randrange(255),random.randrange(255),random.randrange(255))
        draw.point(xy=xy, fill=color)

    # 4.将画布对象转换成字节数据
    buffer = BytesIO() # 缓存
    img.save(buffer, 'png') # 指定的图片格式为png

    # 5. 清场（删除一些对象的引用）
    del draw
    del img

    return buffer.getvalue()  # 从BytesIO对象中获取字节数据


# 验证验证码
def checkCode(request, verifycode):
    # 从session中取出验证码
    chars = request.session['verifycode']
    # 判断验证码是否一致
    if verifycode == chars:
        return True
    else:
        return False

# 生成token
def token():
    md5 = hashlib.md5()
    md5.update(str(uuid.uuid4()).encode())
    return md5.hexdigest()

# 加密
def crypto(str):
    sha1 = hashlib.sha1()
    sha1.update((str+'qfxa').encode())
    return sha1.hexdigest()
import os
from flask import Flask, request, redirect, url_for, jsonify
from flask import send_from_directory
from paddle.vision.datasets import folder
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import secure_filename
from paddleocr import PaddleOCR, draw_ocr
from traceback import print_exc
import json
import uuid
from PIL import Image
from id import IdCard

# Blueprint  蓝图分模块

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['JSON_AS_ASCII'] = False
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': app.config['UPLOAD_FOLDER']
})


def paddle_ocr(path):
    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
    global id_number
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, lang="ch",
                    show_log=True)  # need to run only once to download and load model into memory
    # C:\Users\Tiger\Desktop\flaskProject
    img_path = path
    print(img_path)
    result = ocr.ocr(img_path, cls=True)
    # [[[44.0, 46.0], [310.0, 46.0], [310.0, 87.0], [44.0, 87.0]], ('中公考试日历', 0.97790664)]
    print(result)

    for line in result:
        # print(line)
        pass
        # print(line[1][0])

    if len(result) > 0:
        result_0 = result[0][1][0]
        result_1 = result[1][1][0]
        result_2 = result[2][1][0]
        result_3 = result[3][1][0]
        result_4 = result[4][1][0]
        result_5 = result[5][1][0]
        print(result_0)
        print(result_1)
        print(result_2)
        print(result_3)
        print(result_4)
        print(result_5)

        split = result_0.split("姓名")
        name = split[1]
        print(name)
        # 性别男民族汉
        gender = result_1[2:3]
        ethnic = result_1[5]
        print(gender)
        print(ethnic)

        # 出生1988年1月31日
        born = result_2.split("出生")[1]
        print(born)
        # 住址武汉市硚口区新合村77号
        address = result_3.split("住址")[1]
        print(address)
        # 公民身份号码
        id1 = result_4.split("公民身份号码")[1]
        print(id1)
        id2 = result_5.split("马：")[1]
        print(id2)
        id_number = ''
        if len(id1) != 0:
            id_number = id1
        elif len(id2) != 0:
            id_number = id2

        return IdCard(name=name, gender=gender, ethnic=ethnic,
                      born=born, address=address, id_number=id_number)

    # image = Image.open(img_path).convert('RGB')
    # boxes = [line[0] for line in result]
    # txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    # im_show = draw_ocr(image, boxes, txts, scores, font_path='PaddleOCR/doc/simfang.ttf')
    # im_show = Image.fromarray(im_show)
    # im_show.save('result.jpg')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/image/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os_path_join = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os_path_join)
            folder_ = app.config['UPLOAD_FOLDER'] + "/" + filename
            print(folder_)
            ocr = paddle_ocr(folder_)
            gender = ocr.gender
            print(gender)
            return {
                'msg': "身份证信息",
                'code': 100,
                'data': {
                    "name": ocr.name,
                    "gender": ocr.gender,
                    "ethnic": ocr.ethnic,
                    "born": ocr.born,
                    "address": ocr.address,
                    "id_number": ocr.id_number
                }
            }
        else:
            return "非图片格式，不允许上传"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()
    # paddle_ocr("./static/uploads/111.jpg")

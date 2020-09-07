from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug import secure_filename
from models import call_API

UPLOAD_FOLDER = './static/images/upload'

#アップロードを許可する拡張子
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#appという名前でFlaskオブジェクトをインスタンスか
app = Flask(__name__)
#メッセージ用に任意のキーを設定
app.secret_key = 'flash_key'

#アップロードされたファイルが許可されている拡張子かどうか判断
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#rootにアクセスした時の処理
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #request.filesがない場合
        if 'file' not in request.files:
            flash('ファイルを選択してください')
            return render_template('index.html')

        file = request.files['file']
        #reqest.filesが無効な場合
        if not allowed_file(file.filename):
            flash('PNG, JPEG, またはJPGファイルを選択してください')
            return render_template('index.html')
        #ファイルが有効な場合
        else:
            filename = secure_filename(file.filename) #ファイル名のうち有害な文字を削除
            file_path = os.path.join(UPLOAD_FOLDER, filename) #ファイル名と保存パスを結合
            file.save(file_path)
            return render_template('display_img.html', file_path=file_path)
    else:
        return render_template('index.html')

#推論ボタンを押した時の処理
@app.route('/classify', methods=['GET', 'POST'])
def classify_img():
    if request.method == 'POST':
        file_path = request.form['image']
        data = call_API(file_path)

        return render_template(
                            'classify_img.html',
                            fish_data=data,
                            file_path=file_path
        )
    else:
        return render_template('index.html')

#メインで実行する関数
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
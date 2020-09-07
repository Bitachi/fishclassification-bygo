import flaski.database
import flaski.dbmodels
import http.client, urllib.request, urllib.parse, urllib.error, base64
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

base_url = 'https://fish-classifying.cognitiveservices.azure.com/'
projectID = '6c6790a0-7217-4e75-bded-78048785ac6b'
publish_iteration_name = 'Iteration2'
prediction_key = '9b301bb9eadf46868410fb31fa19d0d1'

# 予想確率の閾値
threshold = 10

#APIの呼び出し
def call_API(uploadFile):
    #予測用インスタントの作成
    prediction_credentials = ApiKeyCredentials(
        in_headers={"Prediction-key": prediction_key}
    )
    predictor = CustomVisionPredictionClient(base_url, prediction_credentials)

    #予測実行
    with open(uploadFile, mode='rb') as f:
        results = predictor.classify_image(projectID, publish_iteration_name, f.read())

    result = []

    for prediction in results.predictions:
        if len(get_fish_data(prediction.tag_name)) != 0:
            #確率が閾値より大きいものを採用
            if prediction.probability * 100 > threshold:
                result.append(get_fish_data(prediction.tag_name))

    return result
 
#魚情報をDBから取得し返す
def get_fish_data(fishname):
    #セッションとテーブルを定義し、セッションを使ってカラムを絞る
    ses = flaski.database.db_session()
    fish_master = flaski.dbmodels.FishMaster
    data = ses.query(fish_master).filter(fish_master.fish_name == fishname).first()

    fish_dict = {}
    
    if not data == None:
        fish_dict['fish_name'] = data.fish_name
        #毒がある場合
        if data.poison == 1:
            fish_dict['poison'] = '毒あり'
            fish_dict['poison_part'] = data.poison_part
        else:
            fish_dict['poison'] = ''
        fish_dict['wiki_url'] = data.wiki_url
        fish_dict['picture_path'] = data.picture_path
        fish_dict['copyright_owner'] = data.copyright_owner
        fish_dict['copyright_url'] = data.copyright_url
    return fish_dict
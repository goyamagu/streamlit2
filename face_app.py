import os
import shutil
from PIL import Image, ImageDraw, ImageFont
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import streamlit as st

# https://qiita.com/s-cat/items/a5b5d213120ef38cc027

# TOML形式で行う
# https://qiita.com/yuu999/items/e56fe82e61db0f74f9cb

# KEY = st.secrets.AzureApiKey.key
# ENDPOINT = st.secrets.AzureApiKey.endpoint
KEY = st.secrets["key"]
ENDPOINT = st.secrets["endpoint"]

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# 認識された顔の上に四角を描く関数
def getAttributesRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top - 20
    right = left + text_w
    bottom = top + text_h
    
    return ((left, top), (right, bottom))

# 認識された顔周辺に四角を描く関数
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))

# 認識された顔の上に属性を描く関数
def getAttributes(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top - 20
    
    return (left, top)

# 画像パスが必要なので、一旦作って、最後消すので、ご安心を
os.makedirs('./tmp_image/', exist_ok=True)

st.set_page_config(layout="wide")

st.title('Face Analysis App')

uploaded_file = st.sidebar.file_uploader('Choose an image', type=['jpg','png'])

selected_attributes = st.sidebar.radio(
     "Choose face_attributes",
     ('age', 'gender', 'glasses', 'smile'))

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    image_path = f'tmp_image/{uploaded_file.name}'
    img.save(image_path)
    
    image_name = uploaded_file.name
    
    # read binary。バイナリファイルの読み込み
    image_data = open(image_path, 'rb')
    
    # 顔の検出
    detected_faces = face_client.face.detect_with_stream(
                        image_data,
                        return_face_landmarks=True,
                        return_face_attributes=['accessories','age','emotion','gender','glasses','hair','makeup','smile'])
    if not detected_faces:
        raise Exception('画像から顔を検出できませんでした。 {}'.format(image_name))
    
    # Face IDをプリント
    print('検出されたFace ID, 画像名=>', image_name, ':')
    for face in detected_faces: print (face.face_id)
    print()

    # イメージオブジェクト生成
    image_data = Image.open(image_path)
    drawing = ImageDraw.Draw(image_data)
    
    # 関数を呼び出して、顔に四角を描く。いまいちJSONがわからない。辞書形式にすることでスマートに書けた。
    for face in detected_faces:
        att = {
            "age" : str(int(face.face_attributes.age)),
            "gender" : face.face_attributes.gender[0:],
            "glasses" : face.face_attributes.glasses[0:],
            "smile" : str(face.face_attributes.smile)
         }
        
        # if selected_attributes == "age":
        #     att = str(int(face.face_attributes.age))
        # elif selected_attributes == "gender":
        #     att = face.face_attributes.gender[0:]
        # elif selected_attributes =="glasses":
        #     att = face.face_attributes.glasses[0:]
        # elif selected_attributes == "smile":
        #     att = str(face.face_attributes.smile)
            
        font = ImageFont.truetype(font='./Helvetica 400.ttf', size=20)
        text_w, text_h = drawing.textsize(att[selected_attributes], font=font)
        drawing.rectangle(getAttributesRectangle(face), fill='Blue')
        drawing.rectangle(getRectangle(face), outline='Blue', width = 3)
        drawing.text(getAttributes(face), att[selected_attributes], fill='White', font=font)
    
    # 画像表示
    st.image(image_data)
    
    # フォルダごと消去
    shutil.rmtree('./tmp_image/')


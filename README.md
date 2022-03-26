## Summary
### azure-cognitiveservices-vision-faceで顔属性を認識するWebAppをStreamlitで実装。Streamlit Sharingで公開
## Reference
- https://docs.microsoft.com/ja-jp/azure/cognitive-services/face/quickstarts/client-libraries?tabs=visual-studio&pivots=programming-language-python
- https://qiita.com/s-cat/items/a5b5d213120ef38cc027
## Note
- AzureのAPIキーをStreamlit Sharingで使いたかったので、StreamlitのSecrets管理機能を使用  
https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
- drawing.textのフォント指定がうまくいかず、Fontファイルもアップロード。デプロイ前はできた。
- UPLOADファイルのパスは取得できないようで、仕方なく、tmpフォルダに保存、消去。デプロイされた後は、どこで処理を行っているかは不明。フォルダを消去する必要はなかったようだ。

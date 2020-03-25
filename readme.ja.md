# clickman
clickman はマウスの移動とクリックをエミュレートできます。  
ゲームの自動デバッグのために作成されました。  

# install
````
cd clickman
pip install -r requirements.txt
````

# how to use
まずは、エミュレートしたい動きを作る必要があります。  
なので、実際にマウスをウィンドウに対して動かしてもらいます。  
以下のコードを実行すると、マウス操作の記録が開始されます。

````
python app/main.py setup
または
python app/main.py setup --output clickman.txt
````

次に、作成した操作を確認します。  
以下のコードでマウスの軌跡を確認できます。

````
python app/main.py test
または
python app/main.py test --input clickman.txt
````

最後に、以下のコマンドで実際に実行できます。

````
python app/main.py run
または
python app/main.py run --input clickman.txt
````
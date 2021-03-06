# KC3 2021 群知能で遊ぶ会
## 概要
2021/09/04, 05のKC3にて行う(予定) 勉強会用のリポジトリ

群知能のうち、粒子群最適化を体験するプログラムが保管されている
## 環境
### OS
Mac Book Air (Intel Core)  
OS mac0S Big Sur 11.5.2  

### Python
python version 3.8.2  

### Modules
pip==21.2.4  
black==21.7b0  
matplotlib==3.4.2 必須  
numpy==1.21.1 必須  
pylint==2.9.6  

## 実行方法
### makeを使用
| コマンド | 説明 |
| --- | --- |
| `$ make test` | アプリケーションを起動する |
| `$ make list` | 必要なモジュールがインストールされいてるか確認する |
| `$ make doc` | ドキュメントを見る |
| `$ make pydoc` | ドキュメントをブラウザで見る |
| `$ make lint` | Lintにかける |
| `$ make zip` | zipにまとめる |
| `$ make clean` | 不要なファイルを消し、きれいにする |

### makeを使わずに実行
`$ python main.py`(カレントディレクトリを`./codes/`とする)

## 使い方
### グラフの見方
プログラムを実行すると、以下のようなウィンドウが表示される。  
<img width="400" alt="description1" src="https://user-images.githubusercontent.com/51152553/130491074-c010a6a3-6573-4ada-b275-cc9d8c387f51.png">  

黄色の散布図が粒子である。  

青色の等高線が目的関数である。白い色の方が値が小さい。  
群はより小さい値を返す地点を探している。

グレーの点が最適解である。

下のバーは何回粒子が移動したかを示しており、スライドすることで動的に変化する。  
注意：素早くスライドさせると描画が追いつかず正しく表示できない場合があるため、ゆっくり動かすこと。　　

### 設定を変更する方法
上部のアプリケーションメニューバーに以下のような項目が表示される。  
<img width="156" alt="スクリーンショット 2021-08-24 2 35 43" src="https://user-images.githubusercontent.com/51152553/130491786-d11ec39d-fb3e-43ce-83b7-db2ea9db310c.png"> 

PSO設定を選択するすると、以下のようなウィンドウが表示される。
<img width="668" alt="スクリーンショット 2021-08-24 2 39 21" src="https://user-images.githubusercontent.com/51152553/130492246-9ba79881-65db-4ad3-be37-ad1a8495c594.png">

それぞれの値を変更し、更新ボタンを押すことで、グラフに反映される。

更新ボタンの上部には関数を選択できるアコーディオンメニューがある。  
いくつかのテスト関数を用意しているので是非試して欲しい。


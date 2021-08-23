# KC3 2021 群知能で遊ぶ会
## 概要
2021/09/04, 05のKC3にて行う勉強会用のリポジトリ

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
matplotlib==3.4.2  
numpy==1.21.1  
pylint==2.9.6  

## 使い方
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
`$ python main.py`(カレントディレクトリをとする`./codes/`)

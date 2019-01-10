ReNomRG GUIの使い方
==================

アプリケーションの起動
------------------

ReNomRGはシングルページウェブアプリケーションです。
インストールが成功している場合、以下のコマンドでアプリケーションを起動することができます。

.. code-block :: shell

    cd workspace # workspaceは任意のディレクトリ。
    renom_rg # このコマンドでReNomRGのGUIが起動します。

``renom_rg``コマンドは、次の引数を与えることができます。

* --host : サーバのIPアドレス
* --port : サーバのポート番号

例えば、ReNomRGを8888ポートで起動する場合は次のコマンドを入力します。

.. code-block :: shell

    renom_rg --port 8888 # ReNomRGを8888ポートで起動する

サーバが起動できると、webブラウザを開き、
サーバのアドレスを入力してください。

.. image:: /_static/image/server_start.png
.. image:: /_static/image/browser.png

するとアプリケーションの画面が表示されます。

データセットの置き方
-----------------

サーバが起動すると、サーバを起動したディレクトリに
``datasrc``, ``storage``, ``scripts``, ``alembic``ディレクトリ、``alembic.ini``ファイルが作成されます。

ディレクトリ構成は以下のようになります。

.. code-block :: shell

<server_start_directory>
    └── alembic.ini        # データベース設定ファイル.
    └── alembic
    |   └── versions       # データベースマイグレーションファイル.
    |   └── env.py         # データベース環境ファイル.
    └── storage
    |   └── storage.db     # デフォルトデータベース(sqlite3).
    |   └── trained_weight # 学習済みweight.
    └── datasrc
    |   └── data.pickle    # 学習&バリデーション用データ.
    |   └── prediction_set
    |       └── pred.pickle # 予測用データ.
    └── scripts
        └── userdefmodel.py # ユーザ定義モデルのスクリプトファイル.(名前は任意に設定可能)


ReNomRGのbetaバージョンで読み込みが可能なデータは"data.pickle"と"pred.pickle"と名付けてください。


データのフォーマット
~~~~~~~~~~~~~~~~

ReNomRGのbetaバージョンでは、pickle化したpandas.DataFrameをアプリケーションに入力することができます。


回帰モデルの作成
-------------

これで、サーバとデータセットが準備できました。それではモデルを開発しましょう。
モデルを作成するには、データセットとハイパーパラメータを設定します。

データセットの作成
~~~~~~~~~~~~~~~

回帰モデルの学習には、学習データとバリデーションデータの作成が必要です。
データセットは学習とモデルの評価のためのバリデーションに用いられます。
ReNomRGでは、学習データセットとバリデーションデータセットはdatasrcディレクトリのデータからランダムにサンプリングされます。

.. image:: /_static/image/dataset.png

上図のように、datasrcからデータセットを作成します。データセットは作成すると変更できません。
Newボタンを押してください。

.. image:: /_static/image/add.png

次のようなページが現れます。

.. image:: /_static/image/setting_dataset.png

データセット名、説明、学習データの比率を選択することができます。
フォームを入力し、confirmボタンを押すと、データセットの確認画面が表示されます。

.. image:: /_static/image/setting_dataset_confirm.png

次のようなグラフが表示されます。データセットに含まれるデータ数や学習データの比率、目的変数のヒストグラムを確認することができます。
データセットを保存するにはsaveボタンを押してください。
データセットページでは、作成したデータセットを確認することができます。データセットページに移動するには次のような操作を行います。

.. image:: /_static/image/menu_dataset.png

.. image:: /_static/image/dataset_page.png

データセット名をクリックすると、データセット内のデータ数や、目的変数のヒストグラムを確認することができます。


ハイパーパラメータの設定
~~~~~~~~~~~~~~~~~~~~

それでは学習を開始しましょう。
モデルを作成するには、Newボタンを押してください。
ハイパーパラメータの設定モーダルが表示されます。

.. image:: /_static/image/setting_params.png


次のパラメータを設定することができます。
Dataset Name: データセット名

CNN architecture: 回帰手法
C-GCNNは変数同士の相関係数を用いたインデックス行列を使って畳み込む変数を取得します。
Kernel-GCNNはガウスカーネルを用いた変数の類似度からインデックス行列を取得し、畳み込む変数を取得します。
DBSCAN-GCNNは変数間のユークリッド距離からインデックス行列を取得し、畳み込む変数を取得します。

Training loop setting: 学習回数とバッチサイス
Batch Size
Total Epoch

Graph Comvolution Params
Number of neighborsはグラフコンボリューションのパラメータです。近傍の数はインデックス行列を取得する際に使います。

学習モデル
~~~~~~~~

ハイパーパラメータの設定が完了したらRunボタンを押してください。
学習が始まると、進捗が表示されます。

.. image:: /_static/image/progress.png

ReNomRGのアンインストール
----------------------

.. code-block :: shell

    pip uninstall renom_rg

ReNomRGは次のコマンドでアンインストールすることができます。

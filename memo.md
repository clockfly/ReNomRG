
# テスト用Webサーバ利用方法

以下の手順でアクセスすると、jsを修正すると自動的にブラウザにロードされます。

Pythonスクリプトを修正した場合には自動ロードされないので、Pythonサーバを再起動する必要があります。


1. 次のコマンドで、Pythonサーバを起動します。

```
python -m renom_rg
```


2. 次のコマンドで、webpack-dev-server を起動します。

```
cd js
npm run start
```

3. ブラウザを起動し、`http://localhost:8090` を表示して webpack-dev-server に接続します。`http://localhost:8090/api` 以下へのアクセスは、`http://localhost:8080` へリダイレクトされます。


# Alembicの使い方

renom\_rgのデータベースは、Alembicでスキーマ管理を行っています。renom\_rgを自動的にAlembicでデータベースを作成するようになっていますが、手動でデータベースを作成する場合は、次のコマンドを実行してください。

```
alembic upgrade head
```

データベースを変更する場合は、renom\_rg/server/db.py を修正し、次のコマンドを実行します。

```
alembic revision --autogenerate -m "<<< 修正内容 >>>"
```

このコマンドは、alembic/versions/ にマイグレーションスクリプトを生成します。スクリプトの内容を確認し、忘れずにgitに登録してください。

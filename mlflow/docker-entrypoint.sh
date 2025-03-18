#!/bin/sh

# MinIO サーバをバックグラウンドで起動
/usr/bin/minio server /data --console-address ":9001" & 

# MinIOの起動を待つ
sleep 10

# MinIO Client (mc) のセットアップ
mc alias set myminio http://127.0.0.1:9000 minio minio123

# mlflowバケットの作成(存在しない場合のみ)
mc ls myminio || mc mb myminio/mlflow

# MinIO サーバプロセスをフォアグラウンドで維持
wait

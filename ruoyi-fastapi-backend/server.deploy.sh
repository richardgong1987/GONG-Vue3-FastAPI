 git push -u origin master -f

ssh root@100.64.0.6 'bash -s' <<EOF
set -e

cd /opt/myapp/GONG-Vue3-FastAPI

git fetch --all
git reset --hard origin/main

cd ruoyi-fastapi-backend

sh build.sh


echo "♻️ Restarting gong-fastapi-backend-1"
docker compose down -v
docker compose up -d --force-recreate

echo "✅ Deployment complete."

EOF



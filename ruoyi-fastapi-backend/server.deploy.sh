 git push -u origin main -f

ssh root@100.64.0.6 'bash -s' <<EOF
set -e

cd /opt/myapp/GONG-Vue3-FastAPI

git fetch --all
git reset --hard origin/main

cd ruoyi-fastapi-backend

sh build.sh


echo "♻️ Restarting server1,server2..."
docker compose down -v
docker compose up -d --force-recreate

echo "✅ Deployment complete."

EOF



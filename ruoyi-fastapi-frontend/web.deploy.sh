 git push -u origin master -f

ssh root@100.64.0.6 'bash -s' <<EOF
set -e

cd /opt/myapp/GONG-Vue3-FastAPI

git fetch --all
git reset --hard origin/master

cd ruoyi-fastapi-frontend

pnpm i

pnpm build:prod
EOF



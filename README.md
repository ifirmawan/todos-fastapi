## Todos

## Get started 
### Without Docker

1. pip install fastapi
2. pip install "uvicorn[standard]"
3. uvicorn app.main:app --reload
4. enjoy!

### With Docker
1. build this docker image
```
docker build -t todos-app .
```
2. run docker image with exposed port
```
docker run -d --name fastapicontainer -p 80:80 todos-app --env-file ./app/.env
```
3. enjoy!

## Deployment

### Deploy to Deta

1. Go to app folder
```
cd app/
```
2. Login Deta account
> I recommended to use google chrome as default browser.
```
deta login
```
3. Deploy this project to Deta
```
deta deploy
```

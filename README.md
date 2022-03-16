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
docker run -d --name fastapicontainer -p 80:80 todos-app
```
3. enjoy!
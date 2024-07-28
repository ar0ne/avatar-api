# API for file uploading to MinIO

- Run docker with MinIO

`docker-compose up -d`

- Open admin page `http://localhost:9001` and create new access key and setup readwrite policies:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::*"
            ]
        }
    ]
}
```

- Add access key and secret key to `.env` file.

- Setup virtual environment and install python dependencies.

- run the app: `fastapi dev main.py`

- Now you could upload and retrieve file from API:

```
curl -F 'file=@/<path/to/folder>/avatar-api/sample.jpg' http://localhost:8000/avatars/upload
```

```
curl http://localhost:8000/avatars/<avatar_id>
curl http://localhost:8000/avatars/<avatar_id>/url
```

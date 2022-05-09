****Running with docker*****

## Configure and run TER project by Armel Sanou

This is a simple way for deploying on server using flask, gunicorn and docker

### Folder Structure 
```
+-- app
|   +-- index.py            // source code of dashboad application
+-- .env                  // configuration about where the app runs
+-- docker-compose.yaml   // build instructions
+-- Dockerfile            // docker image instructions
```

### Commands
```
0. give permission like sudo chmod 777 /var/run/docker.sock to allow connection
1. cd directory where your project is
2. docker-compose build
3. docker-compose up
```
Then, If you built it localy visit: 127.0.0.1:5000 otherwise, use your server ip xxx.xxx.xxx.xxx:5000 to see the dashboard.



##After doing that, you can also navigate to folder named code (projetTer2022/code/), and run pyhton index.py



##Do not forget that, each research you dou within interface generate word into corpus.txt file who is in the current folder.

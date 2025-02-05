docker run -it ^
--env="DISPLAY=host.docker.internal:0" ^
--name lab_rob_container ^
--net=host ^
--privileged ^
--mount type=bind,source=C:\Users\username\lab_rob_shared,target=/home/lab_rob_shared ^
lab_rob_image ^
bash
    
docker rm lab_rob_container

### Steps, I did to solve task #1:
1. docker pull ubuntu
2. docker save -o ubuntu.tar ubuntu
3. docker inspect ubuntu
4. mkdir extracted_ubuntu_image
5. tar -xvzf ubuntu.zip --directory ./extracted_ubuntu_image/ && cd extracted_ubuntu_image/
6. Make some changes, if needed
7. tar -cvzf ../ubuntu.zip ./*
8. cd .. && cat ubuntu.zip | docker load
9. docker inspect ubuntu

### Steps, I did to solve task #1:
1. docker build -t rome_dat .
2. docker run rome_date
FROM Ubuntu
COPY . backend/
WORKDIR backend/
RUN apt-get update && apt-get install -y python3-pip && pip3 install -r requirements.txt && chmod +x boot.sh
ENTRYPOINT ["./boot.sh"]
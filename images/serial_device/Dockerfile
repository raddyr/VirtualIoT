FROM iot/commons

COPY dev-config.json /root/.iot/

ENV DEVICE_CONFIG_FILE /root/.iot/dev-config.json
EXPOSE 22343

CMD ["/bin/bash", "-c", "python /root/.iot/configure.py ; /bin/bash"]


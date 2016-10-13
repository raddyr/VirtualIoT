FROM iot/common_gpio

COPY dev-config.json /root/.iot/
COPY test.py /root/

ENV DEVICE_CONFIG_FILE /root/.iot/dev-config.json
ENV GPIO_0 /dev/gpio0
ENV GPIO_1 /dev/gpio1
ENV GPIO_2 /dev/gpio2

EXPOSE 22343-22345

CMD ["/bin/bash", "-c", "python /root/.iot/configure.py ; python /root/test.py"]


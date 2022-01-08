FROM python:3.7.12-slim

ADD ./ /opt/otree
COPY startup.sh /opt/otree/startup.sh
WORKDIR /opt/otree
EXPOSE 8000

RUN cd /opt/otree && pip install -r requirements_base.txt

ENTRYPOINT ["/opt/otree/startup.sh"]
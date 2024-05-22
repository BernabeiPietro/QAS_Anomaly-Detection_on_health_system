FROM httpd:2.4

COPY ./generate.sh /
RUN /generate.sh
COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./httpd-default.conf /usr/local/apache2/conf/extra/httpd-default.conf
COPY ./malware/malware.sh /
COPY ./malware/ncat /


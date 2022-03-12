FROM ubuntu:focal

RUN apt-get update
#RUN apt-get upgrade
RUN apt -y install python3.9
RUN apt -y install python3-pip
RUN python3.9 -m pip install spacy
RUN python3.9 -m spacy download en_core_web_sm
RUN pip install dash
RUN pip install dash_core_components
RUN pip install dash_html_components
RUN pip install dash_table
RUN pip install "dash-bootstrap-components<1"
RUN pip install pandas
RUN pip install Bio
RUN pip install stop_words
RUN pip install orange3
RUN pip install pyenchant 
RUN pip install Wordcloud
RUN pip install seaborn
RUN pip install nltk
RUN python3 -c "import nltk"
RUN pip install coclust
RUN pip install gunicorn


COPY code/ ./

CMD [ "gunicorn", "--workers=2", "--threads=1", "-b 0.0.0.0:80", "index:server"]

#RUN cd home
#COPY . /home
#WORKDIR /home


#CMD gunicorn -b 0.0.0.0:88 index:server
#CMD [ "python3","index.py"]
#EXPOSE 8088

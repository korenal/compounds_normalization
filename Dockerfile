FROM python:3.8

ADD compounds_normalization.py .

RUN pip install PubChemPy xlsxwriter

ENTRYPOINT ["python", "./compounds_normalization.py"]
CMD ["Adenosine","Adenocard","BG8967","Bivalirudin","BAYT006267","diflucan","ibrutinib","PC-32765"]
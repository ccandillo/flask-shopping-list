git clone https://github.com/tontonDuPirox/flask-shopping-list

cd flask-shopping-list

virtualenv venv

. venv/bin/activate

pip install $(cat requirements.txt)

python shopping-list/shopping-list.py
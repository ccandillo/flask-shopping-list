git clone
cd
virtualenv venv
. venv/activate
pip install $(cat requirements.txt)
cd shopping-list
python shopping-list.py
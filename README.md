# supreme


## Install

```bash
git clone https://github.com/FranktheTank123/supreme.git

cd supreme
virtualenv env
source env/bin/activate
pip install -r requirements.txt

cp chromedriver env/bin # copy chrome driver for Selenium
```

## Daily Data Crawl
```bash
scrapy crawl supreme -o 'supreme.json'
```

## 1-click shop

- follow `config.info_template.py` to create `config.info.py`.
- for testing: `python -i main.py test`
- for real: `python -i main.py`, make sure run at least 1min before the drop, so that you can handle `reCAPTCHA` yourself

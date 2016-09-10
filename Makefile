clean: 
	rm -rf scrapped/*
scrap: clean
	scrapy runspider scrap.py
build:
	pandoc --toc -S -o un_certain_disparate.epub title.html `cat pages.txt`

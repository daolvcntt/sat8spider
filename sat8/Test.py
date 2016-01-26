import re

config_urls = [
    {
        "url" : "http://news.zing.vn/cong-nghe/dien-thoai/trang{{page}}.html",
        "max_page" : 10
    }
]

for url in config_urls:
	if url["max_page"] > 0:
		for i in range(1, url["max_page"]):
			_url = url["url"]
			print _url.replace('{{page}}', str(i))
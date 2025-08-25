# WeatherPredictor

## Web scraper
Download a chromedriver at the link https://googlechromelabs.github.io/chrome-for-testing/#stable.
Since I use a M2 macbook air, the platform is mac-arm64.
```
# Run these in your terminal, from anywhere
sudo rm /usr/local/bin/chromedriver  # remove old one

curl -O (link)
unzip chromedriver-mac-arm64.zip

sudo mv chromedriver-mac-arm64/chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver

chromedriver --version # To verify it matches your chrome browser
```

To check chrome version:
```
chromedriver --version
```

# Future work
<li> Store the data in a database/data warehouse </li>
<li> Use NLP/LLM to have a generative AI chatbot </li>

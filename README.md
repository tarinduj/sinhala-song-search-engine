# Sinhala Song Search Engine using Python + Elasticsearch

This work is inspired by the work at [pycon-2018-pyelasticsearch](https://github.com/julieqiu/pycon-2018-pyelasticsearch) repository.

Follow the below steps to build the search engine locally. The build was only tested on OS X Catalina, hence the instruction are given for OS X.

1. Install [Python 3.6.4] or a higher version.(https://www.python.org/downloads/).

2. Install Elasticsearch 6.x and Kibana 6.x. (Note:[Java](https://java.com/en/download/) may be required.)

  - For OS X, you can use [Homebrew](https://brew.sh/):
```
brew update
brew install kibana@6.8
brew install elasticsearch@6.8

brew services start elasticsearch@6.8
brew services start kibana@6.8
```
  - For Windows or Linux, see the Elastic downloads page for[Elasticsearch](https://www.elastic.co/downloads/elasticsearch) and [Kibana](https://www.elastic.co/downloads/kibana).

  - Make sure you can visit http://localhost:5601/ and http://localhost:9200/ in your browser.

3. Clone the `sinhala-song-search-engine` repository to your computer by running:
```
git clone https://github.com/tarinduj/sinhala-song-search-engine
```

4. In root of the repository, set up a virtualenv:
```
python3 -m venv venv
source venv/bin/activate
```

5. Install the necessary python requirements:
```
pip install -r requirements.txt
```

6. Set up the searchapp:
```
pip install -e .
```

You're all set for the tutorial this Wednesday! :)

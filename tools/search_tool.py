import requests
from langchain.tools import tool
import os
import json


class SearchTools():

    @tool("search internet")
    def search_internet(query):
        """
            Useful to search the internet about a given topic and return relevant results
        """
        return SearchTools.search(query)


    def search(query, n_results=2):
        url="https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()['organic']
        stirng = []
        for result in results[:n_results]:
            try:
                stirng.append('\n'.join([
                    f"Title: {result['title']}", f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}", "\n-----------------"
                ]))
            except KeyError:
                next

        content = '\n'.join(stirng)
        return f"\nSearch result: {content}\n"
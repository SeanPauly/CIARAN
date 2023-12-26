import requests

class WebSearchEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    def search_web(self, query):
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {"q": query, "count": 5}  # You can adjust the count as needed

        response = requests.get(self.endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data.get("webPages", {}).get("value", [])
        else:
            print(f"Error: {response.status_code}")
            return []

def main():
    api_key = "YOUR_BING_API_KEY"  # Replace with your Bing API key
    search_engine = WebSearchEngine(api_key)

    while True:
        query = input("Enter your search query (type 'exit' to quit): ")

        if query.lower() == 'exit':
            break

        search_results = search_engine.search_web(query)

        if search_results:
            print("Search results:")
            for index, result in enumerate(search_results, start=1):
                print(f"{index}. {result['name']} ({result['url']})")
        else:
            print("No results found.")

if __name__ == "__main__":
    main()

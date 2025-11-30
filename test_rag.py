import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def wait_for_server():
    for _ in range(10):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                print("Server is up!")
                return
        except requests.exceptions.ConnectionError:
            pass
        print("Waiting for server...")
        time.sleep(2)
    print("Server failed to start.")
    sys.exit(1)

def test_ingest():
    print("Testing ingestion...")
    with open("data/sample.txt", "rb") as f:
        files = {"file": ("sample.txt", f, "text/plain")}
        response = requests.post(f"{BASE_URL}/ingest", files=files)
    
    if response.status_code == 200:
        print("Ingestion successful:", response.json())
    else:
        print("Ingestion failed:", response.text)
        sys.exit(1)

def test_search():
    print("Testing search...")
    query = "What is Artificial Intelligence?"
    response = requests.get(f"{BASE_URL}/search", params={"query": query})
    
    if response.status_code == 200:
        data = response.json()
        print("Search successful!")
        print("Answer:", data["answer"])
        print("Sources:", data["sources"])
        print("Context:", data["context"][:200] + "...")
    else:
        print("Search failed:", response.text)
        sys.exit(1)

if __name__ == "__main__":
    wait_for_server()
    test_ingest()
    test_search()

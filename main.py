"""
Task 5: External API Integration System
Author: sneb18240602
Description: Fetches data from an external REST API, parses JSON payloads,
             transforms data into domain records, and handles HTTP/network errors.
"""

import json
import urllib.request
import urllib.error

# Public mock REST API endpoint returning collection records
API_URL = "https://jsonplaceholder.typicode.com/posts"


class APIClient:
    """Handles external REST API communication and response validation."""
    
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url

    def fetch_raw_data(self, limit: int = 5) -> list:
        """Sends an HTTP GET request and safely extracts JSON records."""
        url = f"{self.base_url}?_limit={limit}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "NeoStark-API-Client/1.0"}
        )

        try:
            print(f"Connecting to API: {url}...")
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                if status_code == 200:
                    raw_content = response.read().decode("utf-8")
                    data = json.loads(raw_content)
                    print(f"Status: {status_code} OK | Received {len(data)} items.\n")
                    return data
                else:
                    print(f"Failed to fetch data. Server responded with status code: {status_code}")
                    return []
        except urllib.error.HTTPError as e:
            print(f"HTTP Error occurred: {e.code} - {e.reason}")
            return []
        except urllib.error.URLError as e:
            print(f"Network / URL Error: Unable to reach server. Reason: {e.reason}")
            return []
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON response from server.")
            return []
        except Exception as e:
            print(f"Unexpected error during API call: {e}")
            return []


class DataTransformer:
    """Transforms raw API payloads into structured system records."""

    @staticmethod
    def transform_to_records(raw_items: list) -> list:
        """Maps external fields into structured inventory/donation records."""
        transformed = []
        for index, item in enumerate(raw_items, start=1):
            # Clean and normalize external text
            title = item.get("title", "Untitled").capitalize()
            short_name = (title[:22] + "..") if len(title) > 22 else title
            
            # Map into domain record format
            record = {
                "id": f"EXT{index:03d}",
                "name": short_name,
                "category": "External API",
                "quantity": (item.get("id", index) * 10),
                "location": f"Region-{item.get('userId', 1)}",
                "status": "Available" if index % 2 != 0 else "Claimed"
            }
            transformed.append(record)
        return transformed


def display_records(records: list) -> None:
    """Prints records in a clean tabular format."""
    if not records:
        print("No records available to display.")
        return

    print(f"\n{'ID':<8} | {'Name':<25} | {'Category':<15} | {'Quantity':<10} | {'Location':<12} | {'Status':<10}")
    print("-" * 90)
    for r in records:
        print(f"{r['id']:<8} | {r['name']:<25} | {r['category']:<15} | {r['quantity']:<10} | {r['location']:<12} | {r['status']:<10}")


def display_summary(records: list) -> None:
    """Calculates and outputs summary metrics for API transformed data."""
    total = len(records)
    total_qty = sum(r["quantity"] for r in records)
    available = sum(1 for r in records if r["status"].lower() == "available")
    claimed = sum(1 for r in records if r["status"].lower() == "claimed")

    print("\n--- API Ingestion Summary ---")
    print(f"Total Records Ingested: {total}")
    print(f"Total Quantity: {total_qty}")
    print(f"Available Items: {available}")
    print(f"Claimed Items: {claimed}")


def main():
    client = APIClient()
    raw_data = client.fetch_raw_data(limit=5)
    
    if raw_data:
        records = DataTransformer.transform_to_records(raw_data)
        display_records(records)
        display_summary(records)
    else:
        print("Integration failed or no data was returned.")


if __name__ == "__main__":
    main()

from datetime import datetime
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


# Logs a message CRM is alive to /tmp/crm_heartbeat_log.txt
def log_crm_heartbeat():
    try:
        import requests
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"}
        )
        response_data = response.json()
        if 'data' in response_data and 'hello' in response_data['data']:
            with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
                timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
                log_file.write(f"{timestamp} CRM is alive\n")
            print("CRM heartbeat logged successfully.")
        else:
            print("GraphQL endpoint did not return expected data.")
    except Exception as e:
        print(f"Error occurred while logging CRM heartbeat: {e}")
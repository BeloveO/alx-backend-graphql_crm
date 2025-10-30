# script that uses a GraphQL query to find pending orders 
# (order_date within the last week) and logs reminders, 
# scheduled to run daily using a cron job.

from datetime import timedelta, datetime
import requests
import json


# Graphql endpoint URL
GRAPHQL_URL = "http://localhost:8000/graphql"

# Query to get orders from the last 7 days
RECENT_ORDERS_QUERY = """
query GetRecentOrders($startDate: DateTime!, $endDate: DateTime!) {
  orders(filter: {orderDate: "%s"}) {
    id
    customer {
      email
    }
    orderDate
  }
}
"""

def send_order_reminders():
    # calculate date range for the last 7 days
    seven_days_ago = datetime.now() - timedelta(days=7)

    # format query with the date
    formatted_query = RECENT_ORDERS_QUERY % f"{seven_days_ago.isoformat()} to {datetime.now().isoformat()}"

    # initialize GraphQL client
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={'query': formatted_query}
        )
        response.raise_for_status()
        data = response.json()

        # check for errors in the response
        if 'errors' in data:
            print("GraphQL errors:", data['errors'])
            return

        orders = data['data']['orders']

        # log reminders for each order with timestamp
        timestamp = datetime.now().isoformat()
        with open("/tmp/order_reminders_log.txt", "a") as log_file:
            for order in orders:
                order_id = order['id']
                customer_email = order['customer']['email']
                log_file.write(f"{timestamp} - Reminder: Order ID {order_id} for customer {customer_email} is pending.\n")

        # Print success message to console
        print("Order reminders processed!")
    except Exception as e:
        print(f"Error occurred while sending order reminders: {e}")

if __name__ == "__main__":
    send_order_reminders()
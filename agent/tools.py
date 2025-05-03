from langchain.tools import tool
import datetime
import random # For simulating API calls

# --- IMPORTANT SECURITY NOTE ---
# These are PLACEHOLDER tools. Real-world tools interacting with APIs
# MUST have proper authentication, authorization, input validation,
# error handling, and potentially human oversight for critical actions.

@tool
def check_order_status(order_id: str) -> str:
    """
    Looks up the status of a customer's order given the order ID.
    Use this tool ONLY when the user provides a valid order ID.
    """
    print(f"--- TOOL: Checking order status for ID: {order_id} ---")
    # *** Placeholder Logic: Replace with actual API call ***
    # Simulate finding an order or not
    if order_id.startswith("ORD") and len(order_id) == 7:
        statuses = ["Processing", "Shipped", "Delivered", "Delayed", "Cancelled"]
        status = random.choice(statuses)
        if status == "Shipped":
            tracking = f"TRK{random.randint(10000, 99999)}"
            return f"Order {order_id} status is: {status}. Tracking number: {tracking}."
        else:
            return f"Order {order_id} status is: {status}."
    else:
        return f"Could not find order with ID {order_id}. Please ensure the ID is correct."
    # *** End Placeholder Logic ***

@tool
def create_support_ticket(customer_name: str, issue_description: str, contact_email: str) -> str:
    """
    Creates a new support ticket in the system when the user's issue cannot be
    resolved directly and they request a ticket or escalation. Gathers customer name,
    a description of the issue, and their email address.
    """
    print(f"--- TOOL: Creating support ticket ---")
    print(f"  Customer: {customer_name}")
    print(f"  Email: {contact_email}")
    print(f"  Issue: {issue_description}")
    # *** Placeholder Logic: Replace with actual API call to your ticketing system ***
    ticket_id = f"TKT-{random.randint(1000, 9999)}"
    confirmation_message = f"Successfully created support ticket {ticket_id} for {customer_name} regarding '{issue_description[:50]}...'. A confirmation email will be sent to {contact_email}."
    print(f"  Generated Ticket ID: {ticket_id}")
    return confirmation_message
    # *** End Placeholder Logic ***

@tool
def get_current_time() -> str:
    """Returns the current date and time."""
    print("--- TOOL: Getting current time ---")
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Add more tools:
# - lookup_product_info(product_name: str) -> str:
# - check_warranty(serial_number: str) -> str:
# - schedule_callback(phone_number: str, preferred_time: str) -> str:

# List of tools available to the agent
CUSTOMER_SUPPORT_TOOLS = [
    check_order_status,
    create_support_ticket,
    get_current_time,
    # Add other defined tools here
]

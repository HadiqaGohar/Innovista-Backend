import random
from datetime import datetime, timedelta
from database import appointments, save_appointments
from utils import send_confirmation

def generate_local_confirmation(citizen_name: str, service: str, appointment_time: str) -> str:
    """
    Local confirmation message generator (no OpenAI).
    """
    return (
        f"Hello {citizen_name}, your appointment for {service} has been booked "
        f"on {appointment_time}. Please arrive 10 minutes early. "
        "Thank you for using our booking service!"
    )

def book_appointment(citizen_name, service, contact):
    """
    Booking Agent:
    - Assigns random appointment time
    - Saves data to JSON
    - Sends confirmation (local template)
    """
    # Generate appointment time
    appointment_time = datetime.now() + timedelta(
        days=random.randint(0, 3),
        hours=random.randint(9, 17)
    )
    appointment_time_str = appointment_time.strftime("%Y-%m-%d %H:%M")

    # Create form data
    form_data = {
        "citizen_name": citizen_name,
        "service": service,
        "contact": contact,
        "appointment_time": appointment_time_str
    }

    # Save to JSON
    appointments.append(form_data)
    save_appointments()

    # Generate local confirmation message
    confirmation = generate_local_confirmation(citizen_name, service, appointment_time_str)

    # Simulated notification (print or SMS/Email if integrated)
    send_confirmation(contact, confirmation)

    return form_data, confirmation

# -----------------------
# CLI / Standalone testing
if __name__ == "__main__":
    print("=== Booking Agent (Offline) ===\n")

    name = input("Enter citizen name: ")
    service = input("Enter service (e.g., Hospital, Clinic): ")
    contact = input("Enter contact info: ")

    form, msg = book_appointment(name, service, contact)

    print("\n--- Appointment Details ---")
    print(form)
    print("\n--- Confirmation Message ---")
    print(msg)
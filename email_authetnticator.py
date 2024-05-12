import csv
import smtplib
import dns.resolver


def check_email_deliverability(email):
    domain = email.split("@")[1]
    try:
        # Get MX record for the domain
        records = dns.resolver.resolve(domain, "MX")
        mx_record = str(records[0].exchange)

        # Connect to the server
        server = smtplib.SMTP(timeout=10)  # Added timeout for better error handling
        server.set_debuglevel(0)  # No debug messages
        server.connect(mx_record)
        server.helo(domain)  # Greet the server
        server.mail("mate@controllzrt.hu")  # Sender email
        code, message = server.rcpt(email)  # Recipient email
        server.quit()

        # Check the response code
        if code == 250:
            return True, "Email is deliverable.", "Deliverable"
        else:
            return False, "Email is not deliverable.", "Undeliverable"
    except Exception as e:
        return False, str(e), "Error"


# Example usage
# email = "baksai.mihaly@danubisoft.hu"
# is_deliverable, message = check_email_deliverability(email)
# print(message)


def process_csv(file_path):
    with open(file_path, mode="r", newline="") as file:
        reader = csv.reader(file)

        # Process the rows
        for row in reader:
            email = row[0]  # Assume the email is in the first column by default
            result = check_email_deliverability(email)
            print(f"{email}: {result[1]} {result[2]}")


# Example usage
process_csv("email.csv")

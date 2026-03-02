import argparse
from invoice_agent.agent import run_invoice_agent


def main():
    parser = argparse.ArgumentParser(description="Invoice Intake Agent")
    parser.add_argument("--email", required=True, help="Path to input email JSON")
    parser.add_argument("--pdf", required=True, help="Path to invoice PDF")

    args = parser.parse_args()

    try:
        result = run_invoice_agent(email_path=args.email,
                                    pdf_path=args.pdf)
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
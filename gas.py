import re
import asyncio
import aiodns
import aiofiles
from functools import lru_cache

# Initialize asynchronous DNS resolver
resolver = aiodns.DNSResolver()

# Basic regex for validating email syntax
def validate_email_syntax(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

# Asynchronously validate the domain by checking the DNS MX records
@lru_cache(maxsize=500)  # Cache results to avoid redundant lookups
async def validate_domain_mx(domain):
    try:
        # Asynchronous DNS MX lookup
        await resolver.query(domain, 'MX')
        return True
    except aiodns.error.DNSError:
        return False

# Complete email validation function (asynchronous)
async def validate_email_address(email):
    # Step 1: Validate email syntax
    if not validate_email_syntax(email):
        return False, f"{email}: Invalid email syntax"

    # Step 2: Validate email domain using MX records
    domain = email.split('@')[-1]
    if await validate_domain_mx(domain):
        return True, f"{email}: Valid email"
    else:
        return False, f"{email}: Invalid domain or no MX records found"

# Asynchronously process emails from a file and write results
async def process_emails(input_file, output_file):
    async with aiofiles.open(input_file, 'r') as file:
        emails = await file.readlines()

    tasks = []
    results = []
    for email in emails:
        email = email.strip()
        if email:  # Skip empty lines
            tasks.append(validate_email_address(email))

    # Run tasks concurrently
    validations = await asyncio.gather(*tasks)

    # Collect results
    for valid, message in validations:
        results.append(f"{message}\n")

    # Write results to an output file
    async with aiofiles.open(output_file, 'w') as file:
        await file.writelines(results)

# Main function to execute the validation process
async def main():
    input_file = "emails_to_check.txt"  # Replace with your input file
    output_file = "validated_results.txt"  # Replace with your output file
    await process_emails(input_file, output_file)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())

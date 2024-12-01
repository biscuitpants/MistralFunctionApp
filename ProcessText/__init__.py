import logging
import os
import requests
import json
from azure.functions import HttpRequest, HttpResponse

# Load environment variables
API_KEY = os.getenv("MISTRAL_API_KEY")
ENDPOINT = os.getenv("MISTRAL_ENDPOINT")

def main(req: HttpRequest) -> HttpResponse:
    logging.info("Processing request...")

    if req.method == "GET":
        # Human-readable response for GET requests
        html_content = """
        <html>
        <head>
            <title>Mistral Function App</title>
        </head>
        <body>
            <h1>Welcome to the Mistral Function App!</h1>
            <p>This endpoint processes text using Mistral AI.</p>
            <p>To use this API, send a POST request with a JSON body in the following format:</p>
            <pre>
{
    "input": "Your text here"
}
            </pre>
            <p>For example, use <code>curl</code>:</p>
            <pre>
curl -X POST https://mistralfunctionapp123.azurewebsites.net/api/ProcessText -H "Content-Type: application/json" -d '{"input": "Hello, Mistral!"}'
            </pre>
        </body>
        </html>
        """
        return HttpResponse(
            html_content,
            status_code=200,
            mimetype="text/html"
        )

    try:
        # Parse the input from the request body
        req_body = req.get_json()
        input_text = req_body.get("input", "")

        # Validate the input
        if not input_text:
            return HttpResponse(
                "Invalid input. Please provide text in the 'input' field of the JSON body.",
                status_code=400
            )

        # Prepare the request to Mistral API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": input_text}]
        }

        # Send the request to the Mistral API
        response = requests.post(ENDPOINT, headers=headers, json=payload)

        # Handle the API response
        if response.status_code == 200:
            result = response.json()
            return HttpResponse(
                json.dumps(result, indent=2),
                status_code=200,
                mimetype="application/json"
            )
        else:
            return HttpResponse(
                f"Error from Mistral API: {response.text}",
                status_code=response.status_code
            )
    except Exception as e:
        logging.error(f"Error: {e}")
        return HttpResponse(
            "An error occurred while processing your request.",
            status_code=500
        )

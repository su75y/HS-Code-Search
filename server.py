from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas as pd
import json
from urllib.parse import parse_qs, urlparse
import os
import traceback

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        print(f"Received request for path: {self.path}")
        
        if self.path.startswith('/search'):
            self.handle_search()
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def handle_search(self):
        try:
            query = parse_qs(urlparse(self.path).query).get('q', [''])[0].lower()
            print(f"Processing search query: {query}")

            # Get absolute path for Excel file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            excel_path = os.path.join(current_dir, 'hsc_des.xlsx')

            print(f"Current directory: {current_dir}")
            print(f"Looking for Excel file: {excel_path}")
            print(f"Files in directory: {os.listdir(current_dir)}")

            # Check if file exists
            if not os.path.exists(excel_path):
                print(f"Error: {excel_path} not found")
                self.send_error(404, f"File not found: hsc_des.xlsx")
                return

            # Load Excel file with error handling
            try:
                print("Loading hsc_des.xlsx...")
                df = pd.read_excel(excel_path)
                print(f"hsc_des.xlsx columns: {df.columns.tolist()}")
            except Exception as e:
                print(f"Error reading Excel file: {str(e)}")
                self.send_error(500, f"Error reading Excel file: {str(e)}")
                return

            # Try different column name variations
            column_mappings = {
                'HS CODE': 'HS Code',
                'HSCODE': 'HS Code',
                'HSCode': 'HS Code',
                'hs_code': 'HS Code',
                'DESCRIPTION': 'Description',
                'Description': 'Description',
                'description': 'Description'
            }

            # Print original column names
            print("Original column names:", df.columns.tolist())

            # Rename columns if they match any of the variations
            for old_col, new_col in column_mappings.items():
                if old_col in df.columns:
                    df = df.rename(columns={old_col: new_col})

            # Convert column names to string
            df.columns = df.columns.astype(str)

            # Print final column names
            print("Final column names:", df.columns.tolist())

            # Check for required columns
            required_columns = ['Description', 'HS Code']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                error_msg = f"Missing columns: {missing_columns}"
                print(f"Error: {error_msg}")
                self.send_error(400, error_msg)
                return

            # Convert HS Code to string and handle NaN values
            df['HS Code'] = df['HS Code'].fillna('').astype(str)
            df['Description'] = df['Description'].fillna('')

            # Search in both columns
            results = df[
                df['Description'].str.lower().str.contains(query, na=False) |
                df['HS Code'].str.lower().str.contains(query, na=False)
            ]

            json_results = results.to_dict('records')
            print(f"Found {len(json_results)} results")

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(json_results).encode())

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())
            self.send_error(500, f"Internal server error: {str(e)}")

def run_server():
    try:
        port = 8000
        server_address = ('', port)
        httpd = HTTPServer(server_address, CustomHandler)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Starting server on port {port}")
        print(f"Current directory: {current_dir}")
        print("Available files:")
        for file in os.listdir(current_dir):
            print(f"- {file}")
        
        httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {str(e)}")
        print(traceback.format_exc())

if __name__ == '__main__':
    run_server()

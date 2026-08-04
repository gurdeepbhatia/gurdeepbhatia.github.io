import sys
import os
import webbrowser
import threading
import time
from flask import Flask, render_template, jsonify, request
from services.chart_generator import prepare_chart
from config import VERSION


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# Initialize Flask with bundled paths
template_folder = get_resource_path('templates')
static_folder = get_resource_path('static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

# Track last activity time
last_activity_time = time.time()
shutdown_event = threading.Event()


def update_activity():
    """Update the last activity timestamp"""
    global last_activity_time
    last_activity_time = time.time()


def monitor_browser_connection():
    """Monitor browser connections and shutdown if inactive"""
    global last_activity_time
    inactivity_timeout = 1800  # seconds (30 minutes)
    
    print("Browser connection monitor started...")
    print("Server will shutdown 30 minutes after browser is closed.")
    
    while not shutdown_event.is_set():
        time.sleep(1)
        
        # Check if inactive for too long
        inactive_time = time.time() - last_activity_time
        if inactive_time > inactivity_timeout:
            print(f"\nNo browser activity detected for 30 minutes.")
            print("Shutting down server...")
            shutdown_event.set()
            os._exit(0)


@app.before_request
def track_activity():
    """Track activity on every request"""
    update_activity()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/version")
def get_version():
    """API endpoint to get application version"""
    return jsonify({"version": VERSION})


@app.route("/prepare-chart/<chart_type>", methods=["POST"])
def generate_chart(chart_type):
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded."
        })
    
    file = request.files['file']
    
    # Check if file is empty
    if file.filename == '':
        return jsonify({
            "success": False,
            "message": "No file selected."
        })
    
    # Validate file extension
    if not file.filename.endswith('.csv'):
        return jsonify({
            "success": False,
            "message": "Invalid file type. Please upload a CSV file."
        })
    
    # Read file content into memory with proper encoding handling
    try:
        # Reset file pointer
        file.seek(0)
        raw_content = file.read()
        
        # Try UTF-8 with BOM signature first
        try:
            file_content = raw_content.decode('utf-8-sig')
        except UnicodeDecodeError:
            # Try UTF-8 without BOM
            try:
                file_content = raw_content.decode('utf-8')
            except UnicodeDecodeError:
                # Try latin-1 as fallback
                file_content = raw_content.decode('latin-1')
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Invalid CSV file encoding: {str(e)}"
        })
    
    # Pass file content to chart generator
    result = prepare_chart(chart_type, file_content)
    return jsonify(result)


def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5001')


if __name__ == "__main__":
    print("=" * 60)
    print("Chart Preparation Utility - Version " + VERSION)
    print("=" * 60)
    print("\nStarting server...")
    print("Server URL: http://127.0.0.1:5001")
    print("\nBrowser will open automatically...")
    print("Close the browser when done - server will shutdown automatically.")
    print("\nPress Ctrl+C to force quit if needed.")
    print("=" * 60)
    print()
    
    # Start browser opening thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start connection monitor thread
    monitor_thread = threading.Thread(target=monitor_browser_connection, daemon=True)
    monitor_thread.start()
    
    # Run Flask app (disable debug mode for production)
    try:
        app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)
    except OSError as e:
        print(f"\nERROR: Failed to start server - {e}")
        print("Port 5001 may already be in use by another application.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Unexpected error - {e}")
        sys.exit(1)
# start_api.py
"""
Startup script for L1 Pricing Model API
Runs FastAPI server with proper configuration
"""

import uvicorn
import sys
import os

def start_server(host="0.0.0.0", port=8000, reload=True):
    """
    Start the FastAPI server
    
    Args:
        host: Host to bind to (default: 0.0.0.0 for all interfaces)
        port: Port to listen on (default: 8000)
        reload: Enable auto-reload on code changes (default: True)
    """
    
    print("\n" + "=" * 70)
    print("🚀 STARTING L1 PRICING MODEL API SERVER")
    print("=" * 70)
    print(f"\n📍 Server Configuration:")
    print(f"   • Host: {host}")
    print(f"   • Port: {port}")
    print(f"   • Auto-reload: {'Enabled' if reload else 'Disabled'}")
    print(f"\n📚 Access Points:")
    print(f"   • API Root: http://localhost:{port}/")
    print(f"   • Swagger UI: http://localhost:{port}/docs")
    print(f"   • ReDoc: http://localhost:{port}/redoc")
    print(f"   • Health Check: http://localhost:{port}/health")
    print(f"\n🔗 API Endpoint:")
    print(f"   • POST http://localhost:{port}/api/v1/predict")
    print("\n" + "=" * 70 + "\n")
    
    # Check if api_main.py exists
    if not os.path.exists("api_main.py"):
        print("❌ ERROR: api_main.py not found!")
        print("   Please ensure you're running this from the project root directory.")
        sys.exit(1)
    
    try:
        uvicorn.run(
            "api_main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("🛑 SERVER STOPPED BY USER")
        print("=" * 70 + "\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description="Start L1 Pricing Model API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    
    args = parser.parse_args()
    
    start_server(
        host=args.host,
        port=args.port,
        reload=not args.no_reload
    )

# start_api.py
"""
Simple script to start the FastAPI server
"""
import uvicorn

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 STARTING L1 PRICING MODEL API SERVER")
    print("=" * 70)
    print("\n📡 Server will start on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 Alternative Docs: http://localhost:8000/redoc")
    print("\n⏳ Starting server...\n")
    
    uvicorn.run(
        "api_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

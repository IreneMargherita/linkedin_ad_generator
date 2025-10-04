from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.ad_routes import router as ad_router
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('app.log')  # File output
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LinkedIn Ad Generator",
    description="Generate professional LinkedIn advertisements using AI",
    version="1.0.0"
)

logger.info("FastAPI app initialized")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

logger.info("CORS middleware configured")

# Include routers
app.include_router(ad_router)
logger.info("Ad routes included")

# Add explicit OPTIONS handler for CORS preflight
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle CORS preflight requests"""
    return {"message": "OK"}

# Get the path to the frontend build directory
frontend_build_path = Path(__file__).parent.parent / "frontend" / "dist"

# Serve static files (CSS, JS, images) from the frontend build
if frontend_build_path.exists():
    logger.info(f"Frontend build found at: {frontend_build_path}")
    app.mount("/assets", StaticFiles(directory=str(frontend_build_path / "assets")), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the frontend application"""
        logger.info("Serving frontend application")
        index_file = frontend_build_path / "index.html"
        return FileResponse(index_file)
    
    # Define API endpoints BEFORE the catch-all route
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        logger.info("Health check requested")
        api_key_set = bool(os.getenv("OPENAI_API_KEY"))
        logger.info(f"API key configured: {api_key_set}")
        return {
            "status": "healthy",
            "api_key_configured": api_key_set
        }

    # Catch-all route for client-side routing (React Router)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the SPA for all non-API routes"""
        logger.debug(f"Serving SPA route: {full_path}")
        # Don't intercept API routes
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("health"):
            logger.debug(f"API route intercepted: {full_path}")
            return {"error": "Not found"}
        
        # Serve static files if they exist
        file_path = frontend_build_path / full_path
        if file_path.is_file():
            logger.debug(f"Serving static file: {file_path}")
            return FileResponse(file_path)
        
        # Otherwise serve index.html for client-side routing
        logger.debug(f"Serving index.html for SPA route: {full_path}")
        index_file = frontend_build_path / "index.html"
        return FileResponse(index_file)
else:
    logger.warning(f"Frontend build not found at: {frontend_build_path}")
    @app.get("/")
    async def root():
        """Root endpoint - Frontend not built yet"""
        logger.info("Serving API-only root endpoint")
        return {
            "message": "LinkedIn Ad Generator API",
            "status": "running",
            "docs": "/docs",
            "note": "Frontend not built. Run 'npm run build' in the frontend directory."
        }




if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server on host=0.0.0.0, port=8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


from app.api.backtesting_routes import router as backtesting_router
from fastapi import FastAPI`r`nfrom app.api.historical_routes import router as historical_router
from app.api.routes import router
from app.api.live_data_routes import (
    router as live_data_router,
)
from app.api.database_routes import (
    router as database_router,
)
from app.api.analytics_routes import (
    router as analytics_router,
)
from database.connection import Database
database = Database()
database.initialize()
app = FastAPI(
    title="ISMAIL Future AI",
    version="1.0.0",
    description=(
        "Future prediction system with "
        "live data, evidence, historical "
        "database and analytics."
    ),
)
app.include_router(automatic_future_routes.router)

app.include_router(
    router,
    prefix="/api",
)
app.include_router(automatic_future_routes.router)

app.include_router(
    live_data_router,
    prefix="/api",
)
app.include_router(automatic_future_routes.router)

app.include_router(
    database_router,
    prefix="/api",
)
app.include_router(automatic_future_routes.router)

app.include_router(
    analytics_router,
    prefix="/api",
)
@app.get("/")
def root():
    return {
        "name": "ISMAIL Future AI",
        "status": "online",
        "version": "0.6.0",
        "systems": [
            "prediction",
            "evidence",
            "live_data",
            "historical_database",
            "trend_analysis",
            "anomaly_detection",
            "data_quality",
        ],
    }



from app.api.feedback_routes import router as feedback_router
from app.api.future_system_routes import router as future_system_router

app.include_router(automatic_future_routes.router)

app.include_router(feedback_router)`r`napp.include_router(automatic_future_routes.router)

app.include_router(backtesting_router)
app.include_router(automatic_future_routes.router)

app.include_router(future_system_router)`r`napp.include_router(automatic_future_routes.router)

app.include_router(backtesting_router)






app.include_router(historical_router)


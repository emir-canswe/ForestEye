from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.pipeline.fetchers.firms import FirmsFetcher
from app.pipeline.fetchers.weather import WeatherFetcher
from app.pipeline.processors.risk_engine import calculate_risk_score, get_risk_level
from app.core.database import SessionLocal
from app.models.db.models import GridCell, RiskScore, ActiveFire
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def run_pipeline():
    """
    Ana veri işleme boru hattı (Pipeline):
    1. Verileri çek (Hava Durumu, NASA FIRMS)
    2. Her grid hücresi için riski hesapla
    3. Veritabanına kaydet
    """
    logger.info("Starting data pipeline...")
    db = SessionLocal()
    
    try:
        weather_fetcher = WeatherFetcher()
        firms_fetcher = FirmsFetcher()
        
        # In a real-world scenario, you would want to optimize this to fetch
        # weather for regions/cities instead of every single 10km grid cell
        # to avoid hitting API rate limits.
        
        cells = db.query(GridCell).all()
        logger.info(f"Processing {len(cells)} grid cells...")
        
        # TODO: Fetch Active Fires and update ActiveFire table
        
        for cell in cells:
            # Example: Fetching weather for this specific cell's center
            # NOTE: For MVP we might want to mock or use a generalized weather if API limits hit
            weather_data = await weather_fetcher.fetch_current_weather(cell.lat_center, cell.lon_center)
            
            # Default values if API fails
            temp = 25
            humidity = 50
            wind_speed = 5
            wind_deg = 0
            
            if weather_data and "main" in weather_data:
                temp = weather_data["main"].get("temp", temp)
                humidity = weather_data["main"].get("humidity", humidity)
                wind_speed = weather_data.get("wind", {}).get("speed", wind_speed)
                wind_deg = weather_data.get("wind", {}).get("deg", wind_deg)
                
            data = {
                "temp": temp,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "ndvi": 0.5, # Mock NDVI for MVP
                "dry_days": 5, # Mock
                "historical_fire_count": 0
            }
            
            score = calculate_risk_score(data)
            level = get_risk_level(score)
            
            new_risk = RiskScore(
                grid_cell_id=cell.id,
                risk_score=score,
                risk_level=level,
                humidity=humidity,
                wind_speed=wind_speed,
                wind_deg=wind_deg,
                temperature=temp,
                ndvi=data["ndvi"],
                dry_days=data["dry_days"]
            )
            
            db.add(new_risk)
            
        db.commit()
        logger.info("Pipeline completed successfully.")
        
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_pipeline, 
        'interval', 
        minutes=settings.RISK_CHECK_INTERVAL_MINUTES,
        id='main_pipeline',
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"Scheduler started with {settings.RISK_CHECK_INTERVAL_MINUTES} min interval")
    return scheduler

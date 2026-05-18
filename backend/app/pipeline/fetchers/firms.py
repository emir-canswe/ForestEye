import httpx
import pandas as pd
from io import StringIO
from app.core.config import settings
from datetime import datetime

class FirmsFetcher:
    def __init__(self):
        self.api_key = settings.NASA_FIRMS_API_KEY
        self.base_url = "https://firms.modaps.eosdis.nasa.gov/api"
        
    async def fetch_active_fires(self, region="TR", days=1) -> pd.DataFrame:
        """
        Fetches active fires from NASA FIRMS VIIRS_SNPP_NRT source for a region.
        Default region is TR (Turkey), last 1 day.
        """
        url = f"{self.base_url}/area/csv/{self.api_key}/VIIRS_SNPP_NRT/{region}/{days}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                
                # The response is a CSV string
                csv_data = StringIO(response.text)
                df = pd.read_csv(csv_data)
                
                # FIRMS CSV typically has columns like: 
                # latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,instrument,confidence,version,bright_ti5,frp,daynight
                return df
                
            except httpx.HTTPError as e:
                print(f"Error fetching FIRMS data: {e}")
                return pd.DataFrame()
            except Exception as e:
                print(f"Unexpected error in FIRMS fetcher: {e}")
                return pd.DataFrame()

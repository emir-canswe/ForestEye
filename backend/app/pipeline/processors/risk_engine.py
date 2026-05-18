from typing import Dict, Any

def calculate_risk_score(data: Dict[str, Any]) -> float:
    """
    Tüm parametreler 0-100 arasına normalize edilir.
    Ağırlıklar alan uzmanlarıyla belirlenmiştir.
    
    Beklenen data formatı:
    {
        "humidity": float,           # %
        "wind_speed": float,         # m/s
        "temp": float,               # °C
        "ndvi": float,               # 0.0 - 1.0 (Bitki örtüsü yoğunluğu)
        "dry_days": int,             # gün
        "historical_fire_count": int # adet
    }
    """
    
    # Nem (ters orantılı: düşük nem = yüksek risk)
    humidity_score = max(0, 100 - data.get("humidity", 50))

    # Rüzgar hızı (0-30 m/s -> 0-100)
    wind_speed = data.get("wind_speed", 0)
    wind_score = min(100, (wind_speed / 30.0) * 100)

    # Sıcaklık (20°C altı = 0, 45°C üstü = 100)
    temp = data.get("temp", 20)
    temp_score = max(0, min(100, ((temp - 20) / 25.0) * 100))

    # Bitki örtüsü yoğunluğu - NDVI (0.0-1.0 -> 0-100)
    # Varsayılan 0.5 (ortalama) kabul edelim
    vegetation_score = data.get("ndvi", 0.5) * 100

    # Yağışsız gün sayısı (0-30 gün -> 0-100)
    dry_days_score = min(100, (data.get("dry_days", 0) / 30.0) * 100)

    # Tarihsel risk (bu bölgede geçmişte yangın olduysa bonus)
    historical_bonus = 20 if data.get("historical_fire_count", 0) > 0 else 0

    # Ağırlıklı toplam
    score = (
        humidity_score    * 0.30 +
        wind_score        * 0.20 +
        temp_score        * 0.20 +
        vegetation_score  * 0.15 +
        dry_days_score    * 0.15
    ) + historical_bonus

    return min(100.0, round(score, 2))

def get_risk_level(score: float) -> str:
    """
    Skora göre risk seviyesini döndürür.
    """
    if score >= 85:
        return "critical"
    elif score >= 70:
        return "high"
    elif score >= 40:
        return "medium"
    return "low"

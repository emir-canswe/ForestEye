import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, GeoJSON, ZoomControl } from 'react-leaflet'
import axios from 'axios'
import toast from 'react-hot-toast'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/v1'

const RiskMap = () => {
  const [riskData, setRiskData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchRiskData = async () => {
      try {
        // Since we don't have DB populated yet in this stage, we might get an empty FeatureCollection
        // But this is how we will fetch it.
        const response = await axios.get(`${API_URL}/risk/current`)
        setRiskData(response.data)
      } catch (error) {
        console.error("Error fetching risk data:", error)
        toast.error("Risk verileri yüklenemedi.")
      } finally {
        setLoading(false)
      }
    }

    fetchRiskData()
  }, [])

  const getRiskColor = (score: number) => {
    if (score >= 85) return '#DC2626' // Critical
    if (score >= 70) return '#EA580C' // High
    if (score >= 40) return '#D97706' // Medium
    return '#16A34A' // Low
  }

  const style = (feature: any) => {
    return {
      fillColor: getRiskColor(feature.properties.risk_score),
      weight: 1,
      opacity: 0.5,
      color: '#374151',
      fillOpacity: 0.4,
    }
  }

  const onEachFeature = (feature: any, layer: any) => {
    const { il_adi, ilce_adi, risk_score, risk_level } = feature.properties
    layer.bindTooltip(`
      <div class="p-1">
        <div class="font-bold text-gray-100">${il_adi || 'Bilinmiyor'} ${ilce_adi ? `/ ${ilce_adi}` : ''}</div>
        <div class="text-sm mt-1">Risk Skoru: <span class="font-bold">${risk_score.toFixed(1)}</span></div>
        <div class="text-xs text-gray-400 mt-1 capitalize">Seviye: ${risk_level}</div>
      </div>
    `, { sticky: true, className: 'bg-gray-800 border-gray-700' })
  }

  return (
    <div className="h-full w-full relative">
      {loading && (
        <div className="absolute inset-0 z-[1000] flex items-center justify-center bg-gray-900/50 backdrop-blur-sm">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
        </div>
      )}
      <MapContainer 
        center={[38.9637, 35.2433]} // Center of Turkey
        zoom={6} 
        zoomControl={false}
        className="h-full w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        <ZoomControl position="bottomright" />
        
        {riskData && riskData.features && riskData.features.length > 0 && (
          <GeoJSON 
            data={riskData} 
            style={style} 
            onEachFeature={onEachFeature} 
          />
        )}
      </MapContainer>
    </div>
  )
}

export default RiskMap

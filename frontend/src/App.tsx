import { Toaster } from 'react-hot-toast'
import RiskMap from './components/Map/RiskMap'

function App() {
  return (
    <div className="h-screen w-full flex flex-col bg-gray-900 overflow-hidden text-gray-100">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-gray-800/80 backdrop-blur-md border-b border-gray-700 p-4 flex justify-between items-center z-10">
        <div className="flex items-center gap-3">
          <div className="text-risk-high text-2xl">🔥</div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-orange-400 to-red-500 bg-clip-text text-transparent">
            ForestEye
          </h1>
          <span className="text-xs px-2 py-1 bg-gray-700 rounded-full text-gray-300 border border-gray-600">Canlı Sistem</span>
        </div>
        
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            <span className="text-gray-400">Son Güncelleme: Az Önce</span>
          </div>
          <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors border border-gray-600">
            Giriş Yap
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 relative flex">
        {/* Left Panel */}
        <aside className="w-80 bg-gray-800/90 backdrop-blur-sm border-r border-gray-700 z-10 flex flex-col hidden md:flex">
          <div className="p-4 border-b border-gray-700">
            <h2 className="font-semibold text-gray-200">Kritik Bölgeler</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
            {/* Placeholder for list */}
            <div className="p-3 bg-gray-700/50 rounded-lg border border-red-900/50 hover:bg-gray-700 cursor-pointer transition-colors">
              <div className="flex justify-between items-start">
                <div>
                  <div className="font-medium text-red-400">Muğla / Bodrum</div>
                  <div className="text-xs text-gray-400 mt-1">Nem: %18 | Rüzgar: 12m/s</div>
                </div>
                <div className="text-xl font-bold text-red-500">87</div>
              </div>
            </div>
            
             <div className="p-3 bg-gray-700/50 rounded-lg border border-orange-900/50 hover:bg-gray-700 cursor-pointer transition-colors">
              <div className="flex justify-between items-start">
                <div>
                  <div className="font-medium text-orange-400">Antalya / Manavgat</div>
                  <div className="text-xs text-gray-400 mt-1">Nem: %22 | Rüzgar: 15m/s</div>
                </div>
                <div className="text-xl font-bold text-orange-500">74</div>
              </div>
            </div>
          </div>
        </aside>

        {/* Map Area */}
        <div className="flex-1 relative bg-gray-900">
          <RiskMap />
        </div>
        
      </main>
    </div>
  )
}

export default App

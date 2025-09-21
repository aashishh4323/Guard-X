import { useState, useEffect } from 'react';
import { MapPin, AlertTriangle, Users, Car } from 'lucide-react';

export default function ThreatHeatmap() {
  const [heatmapData, setHeatmapData] = useState([]);
  const [selectedZone, setSelectedZone] = useState(null);

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <MapPin className="w-6 h-6 text-emerald-400" />
          Threat Intelligence Map
        </h3>
        <div className="flex gap-2">
          <button className="px-3 py-1 bg-emerald-600 text-white rounded text-sm">Live</button>
          <button className="px-3 py-1 bg-slate-600 text-white rounded text-sm">24H</button>
        </div>
      </div>
      
      {/* Interactive Map Container */}
      <div className="h-96 bg-slate-900 rounded-lg relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/10 to-red-500/10"></div>
        
        {/* Threat Zones */}
        <div className="absolute top-4 left-4 space-y-2">
          <div className="flex items-center gap-2 text-sm">
            <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
            <span className="text-red-400">Critical Zones</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
            <span className="text-yellow-400">Medium Risk</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-green-400">Safe Zones</span>
          </div>
        </div>
      </div>
    </div>
  );
}
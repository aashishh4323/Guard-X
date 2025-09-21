import { useState, useEffect } from 'react';
import { Bell, AlertTriangle, CheckCircle, Clock, MapPin, Users } from 'lucide-react';

export default function AlertCenter() {
  const [alerts, setAlerts] = useState([]);
  const [filter, setFilter] = useState('all');

  const alertTypes = {
    'CRITICAL': { color: 'red', icon: AlertTriangle },
    'HIGH': { color: 'orange', icon: AlertTriangle },
    'MEDIUM': { color: 'yellow', icon: Bell },
    'LOW': { color: 'green', icon: Bell }
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Bell className="w-6 h-6 text-emerald-400" />
          Alert Management Center
        </h3>
        
        <div className="flex gap-2">
          {['all', 'critical', 'high', 'medium', 'low'].map(type => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`px-3 py-1 rounded text-sm capitalize ${
                filter === type 
                  ? 'bg-emerald-600 text-white' 
                  : 'bg-slate-600 text-gray-300 hover:bg-slate-500'
              }`}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-4 max-h-96 overflow-y-auto">
        {alerts.map((alert, index) => {
          const AlertIcon = alertTypes[alert.level]?.icon || Bell;
          const colorClass = alertTypes[alert.level]?.color || 'gray';
          
          return (
            <div key={index} className={`border-l-4 border-${colorClass}-500 bg-slate-700/50 p-4 rounded-r-lg`}>
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  <AlertIcon className={`w-5 h-5 text-${colorClass}-400 mt-1`} />
                  <div>
                    <h4 className="font-semibold text-white">{alert.title}</h4>
                    <p className="text-gray-300 text-sm mt-1">{alert.description}</p>
                    
                    <div className="flex items-center gap-4 mt-2 text-xs text-gray-400">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {alert.timestamp}
                      </span>
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3 h-3" />
                        {alert.location}
                      </span>
                      <span className="flex items-center gap-1">
                        <Users className="w-3 h-3" />
                        {alert.detectionCount} detected
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <button className="px-3 py-1 bg-emerald-600 text-white rounded text-sm hover:bg-emerald-700">
                    Acknowledge
                  </button>
                  <button className="px-3 py-1 bg-slate-600 text-white rounded text-sm hover:bg-slate-700">
                    Dismiss
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
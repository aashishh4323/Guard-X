import { useState, useEffect } from 'react';
import { Smartphone, Wifi, Battery, Signal } from 'lucide-react';

export default function MobileAlerts() {
  const [mobileStatus, setMobileStatus] = useState({
    connected: true,
    battery: 85,
    signal: 'strong',
    notifications: 12
  });

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
      <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
        <Smartphone className="w-6 h-6 text-emerald-400" />
        Mobile Command Center
      </h3>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="text-center">
          <Wifi className={`w-8 h-8 mx-auto mb-2 ${mobileStatus.connected ? 'text-green-400' : 'text-red-400'}`} />
          <p className="text-sm text-gray-300">Connection</p>
          <p className="text-xs text-emerald-400">{mobileStatus.connected ? 'Online' : 'Offline'}</p>
        </div>
        
        <div className="text-center">
          <Battery className="w-8 h-8 mx-auto mb-2 text-green-400" />
          <p className="text-sm text-gray-300">Battery</p>
          <p className="text-xs text-emerald-400">{mobileStatus.battery}%</p>
        </div>
        
        <div className="text-center">
          <Signal className="w-8 h-8 mx-auto mb-2 text-green-400" />
          <p className="text-sm text-gray-300">Signal</p>
          <p className="text-xs text-emerald-400 capitalize">{mobileStatus.signal}</p>
        </div>
        
        <div className="text-center">
          <div className="w-8 h-8 mx-auto mb-2 bg-emerald-400 rounded-full flex items-center justify-center text-slate-900 font-bold">
            {mobileStatus.notifications}
          </div>
          <p className="text-sm text-gray-300">Alerts</p>
          <p className="text-xs text-emerald-400">Pending</p>
        </div>
      </div>

      <div className="space-y-3">
        <button className="w-full bg-emerald-600 hover:bg-emerald-700 text-white py-2 px-4 rounded-lg transition-colors">
          Send Test Alert
        </button>
        <button className="w-full bg-slate-600 hover:bg-slate-700 text-white py-2 px-4 rounded-lg transition-colors">
          Configure Push Notifications
        </button>
      </div>
    </div>
  );
}
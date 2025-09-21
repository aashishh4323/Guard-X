import { useState, useEffect } from 'react';
import { Shield, Wifi, Signal, AlertTriangle, CheckCircle, Radio, Zap } from 'lucide-react';

export default function AntiJammingDashboard() {
  const [jammingStatus, setJammingStatus] = useState({
    monitoring: false,
    jamming_detected: false,
    current_channel: 'wifi',
    signal_strength: null,
    network_health: {},
    last_update: null
  });

  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch('/api/security/jamming-status');
        const data = await response.json();
        setJammingStatus(data.anti_jamming_status);
      } catch (error) {
        console.error('Failed to fetch jamming status:', error);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const startMonitoring = async () => {
    try {
      await fetch('/api/security/start-monitoring', { method: 'POST' });
      setJammingStatus(prev => ({ ...prev, monitoring: true }));
    } catch (error) {
      console.error('Failed to start monitoring:', error);
    }
  };

  const testJammingDetection = async () => {
    try {
      await fetch('/api/security/test-jamming', { method: 'POST' });
      alert('Jamming detection test initiated!');
    } catch (error) {
      console.error('Test failed:', error);
    }
  };

  return (
    <div className="space-y-6">
      {/* Status Overview */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <Shield className="w-6 h-6 text-emerald-400" />
            Anti-Jamming Defense System
          </h3>
          
          <div className="flex gap-3">
            <button
              onClick={startMonitoring}
              disabled={jammingStatus.monitoring}
              className="bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-600 text-white px-4 py-2 rounded-lg flex items-center gap-2"
            >
              <Zap className="w-4 h-4" />
              {jammingStatus.monitoring ? 'Monitoring Active' : 'Start Monitoring'}
            </button>
            
            <button
              onClick={testJammingDetection}
              className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg"
            >
              Test System
            </button>
          </div>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-700/50 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">System Status</p>
                <p className={`text-lg font-bold ${jammingStatus.monitoring ? 'text-green-400' : 'text-gray-400'}`}>
                  {jammingStatus.monitoring ? 'ACTIVE' : 'INACTIVE'}
                </p>
              </div>
              {jammingStatus.monitoring ? 
                <CheckCircle className="w-8 h-8 text-green-400" /> : 
                <AlertTriangle className="w-8 h-8 text-gray-400" />
              }
            </div>
          </div>

          <div className="bg-slate-700/50 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Threat Level</p>
                <p className={`text-lg font-bold ${
                  jammingStatus.jamming_detected ? 'text-red-400' : 'text-green-400'
                }`}>
                  {jammingStatus.jamming_detected ? 'DETECTED' : 'CLEAR'}
                </p>
              </div>
              <AlertTriangle className={`w-8 h-8 ${
                jammingStatus.jamming_detected ? 'text-red-400' : 'text-green-400'
              }`} />
            </div>
          </div>

          <div className="bg-slate-700/50 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Active Channel</p>
                <p className="text-lg font-bold text-emerald-400 uppercase">
                  {jammingStatus.current_channel}
                </p>
              </div>
              <Radio className="w-8 h-8 text-emerald-400" />
            </div>
          </div>

          <div className="bg-slate-700/50 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Signal Strength</p>
                <p className="text-lg font-bold text-emerald-400">
                  {jammingStatus.signal_strength?.wifi || 'N/A'} dBm
                </p>
              </div>
              <Signal className="w-8 h-8 text-emerald-400" />
            </div>
          </div>
        </div>
      </div>

      {/* Signal Monitoring */}
      <div className="grid lg:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
          <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Wifi className="w-5 h-5 text-emerald-400" />
            Signal Analysis
          </h4>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-300">WiFi Signal</span>
              <div className="flex items-center gap-2">
                <div className="w-32 bg-slate-700 rounded-full h-2">
                  <div 
                    className="bg-emerald-400 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${Math.max(0, 100 - (jammingStatus.signal_strength?.wifi || 50))}%` }}
                  ></div>
                </div>
                <span className="text-emerald-400 text-sm">
                  {jammingStatus.signal_strength?.wifi || 'N/A'} dBm
                </span>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-gray-300">Cellular Signal</span>
              <div className="flex items-center gap-2">
                <div className="w-32 bg-slate-700 rounded-full h-2">
                  <div 
                    className="bg-blue-400 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${Math.max(0, 100 - (jammingStatus.signal_strength?.cellular || 60))}%` }}
                  ></div>
                </div>
                <span className="text-blue-400 text-sm">
                  {jammingStatus.signal_strength?.cellular || 'N/A'} dBm
                </span>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-gray-300">Packet Loss</span>
              <span className={`font-bold ${
                (jammingStatus.network_health?.packet_loss || 0) > 10 ? 'text-red-400' : 'text-green-400'
              }`}>
                {jammingStatus.network_health?.packet_loss?.toFixed(1) || '0.0'}%
              </span>
            </div>
          </div>
        </div>

        {/* Countermeasures */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
          <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-emerald-400" />
            Active Countermeasures
          </h4>
          
          <div className="space-y-3">
            {[
              { name: 'Frequency Hopping', active: jammingStatus.jamming_detected },
              { name: 'Channel Switching', active: jammingStatus.current_channel !== 'wifi' },
              { name: 'Power Boost', active: false },
              { name: 'Backup Channels', active: true }
            ].map((measure, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-gray-300">{measure.name}</span>
                <div className={`px-2 py-1 rounded text-xs font-bold ${
                  measure.active 
                    ? 'bg-green-600 text-white' 
                    : 'bg-slate-600 text-gray-300'
                }`}>
                  {measure.active ? 'ACTIVE' : 'STANDBY'}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Alerts */}
      {alerts.length > 0 && (
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
          <h4 className="text-lg font-bold text-white mb-4">Recent Jamming Alerts</h4>
          <div className="space-y-2">
            {alerts.map((alert, index) => (
              <div key={index} className="bg-red-900/20 border border-red-500/30 rounded-lg p-3">
                <div className="flex items-center justify-between">
                  <span className="text-red-400 font-medium">{alert.type}</span>
                  <span className="text-gray-400 text-sm">{alert.timestamp}</span>
                </div>
                <p className="text-gray-300 text-sm mt-1">{alert.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
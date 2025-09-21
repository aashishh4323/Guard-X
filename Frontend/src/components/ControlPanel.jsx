import { useState } from 'react';
import { Settings, Sliders, Target, Shield, Zap, Brain } from 'lucide-react';

export default function ControlPanel() {
  const [settings, setSettings] = useState({
    confidenceThreshold: 0.7,
    alertSensitivity: 'medium',
    autoResponse: true,
    faceRecognition: true,
    behaviorAnalysis: true,
    threatPrediction: false
  });

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
      <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
        <Settings className="w-6 h-6 text-emerald-400" />
        AI Control Panel
      </h3>

      <div className="space-y-6">
        {/* Detection Settings */}
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-emerald-400 flex items-center gap-2">
            <Target className="w-5 h-5" />
            Detection Parameters
          </h4>
          
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Confidence Threshold: {(settings.confidenceThreshold * 100).toFixed(0)}%
              </label>
              <input
                type="range"
                min="0.1"
                max="1"
                step="0.05"
                value={settings.confidenceThreshold}
                onChange={(e) => setSettings({...settings, confidenceThreshold: parseFloat(e.target.value)})}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Alert Sensitivity</label>
              <select 
                value={settings.alertSensitivity}
                onChange={(e) => setSettings({...settings, alertSensitivity: e.target.value})}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white"
              >
                <option value="low">Low - Fewer alerts</option>
                <option value="medium">Medium - Balanced</option>
                <option value="high">High - Maximum sensitivity</option>
              </select>
            </div>
          </div>
        </div>

        {/* AI Features */}
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-emerald-400 flex items-center gap-2">
            <Brain className="w-5 h-5" />
            AI Features
          </h4>
          
          <div className="space-y-3">
            {[
              { key: 'autoResponse', label: 'Auto Response System', icon: Zap },
              { key: 'faceRecognition', label: 'Facial Recognition', icon: Shield },
              { key: 'behaviorAnalysis', label: 'Behavior Analysis', icon: Brain },
              { key: 'threatPrediction', label: 'Threat Prediction', icon: Target }
            ].map(({ key, label, icon: Icon }) => (
              <div key={key} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Icon className="w-4 h-4 text-emerald-400" />
                  <span className="text-gray-300">{label}</span>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings[key]}
                    onChange={(e) => setSettings({...settings, [key]: e.target.checked})}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-slate-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
                </label>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
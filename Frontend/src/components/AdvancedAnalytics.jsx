import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, AlertTriangle, Users, Activity, Shield, Target } from 'lucide-react';

export default function AdvancedAnalytics() {
  const [analyticsData, setAnalyticsData] = useState({
    threatTrends: [],
    detectionAccuracy: 94.5,
    responseTime: 2.3,
    falsePositiveRate: 3.2,
    systemUptime: 99.8
  });

  const threatLevelData = [
    { name: 'Critical', value: 12, color: '#ef4444' },
    { name: 'High', value: 28, color: '#f97316' },
    { name: 'Medium', value: 45, color: '#eab308' },
    { name: 'Low', value: 89, color: '#22c55e' }
  ];

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-emerald-400 text-sm font-medium">Detection Accuracy</p>
              <p className="text-3xl font-bold text-white">{analyticsData.detectionAccuracy}%</p>
            </div>
            <Target className="w-8 h-8 text-emerald-400" />
          </div>
          <div className="mt-4 flex items-center text-sm">
            <TrendingUp className="w-4 h-4 text-green-400 mr-1" />
            <span className="text-green-400">+2.1% from last week</span>
          </div>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-emerald-400 text-sm font-medium">Avg Response Time</p>
              <p className="text-3xl font-bold text-white">{analyticsData.responseTime}s</p>
            </div>
            <Activity className="w-8 h-8 text-emerald-400" />
          </div>
          <div className="mt-4 flex items-center text-sm">
            <TrendingUp className="w-4 h-4 text-green-400 mr-1" />
            <span className="text-green-400">-0.5s improvement</span>
          </div>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-emerald-400 text-sm font-medium">System Uptime</p>
              <p className="text-3xl font-bold text-white">{analyticsData.systemUptime}%</p>
            </div>
            <Shield className="w-8 h-8 text-emerald-400" />
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-green-400">Operational</span>
          </div>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-emerald-400 text-sm font-medium">False Positive Rate</p>
              <p className="text-3xl font-bold text-white">{analyticsData.falsePositiveRate}%</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-emerald-400" />
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-green-400">Within acceptable range</span>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Threat Distribution */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
          <h3 className="text-xl font-bold text-white mb-4">Threat Level Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={threatLevelData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}`}
              >
                {threatLevelData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Trend Analysis */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-emerald-500/20 p-6">
          <h3 className="text-xl font-bold text-white mb-4">Detection Trends (24H)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analyticsData.threatTrends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: '1px solid #10b981',
                  borderRadius: '8px'
                }}
              />
              <Line type="monotone" dataKey="detections" stroke="#10b981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
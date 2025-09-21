import asyncio
import time
import numpy as np
import threading
from datetime import datetime, timedelta
import psutil
import socket
import subprocess
import json

class AntiJammingSystem:
    def __init__(self):
        self.is_monitoring = False
        self.jamming_detected = False
        self.signal_strength_history = []
        self.network_health = {}
        self.backup_channels = ['wifi', 'cellular', 'ethernet']
        self.current_channel = 'wifi'
        self.alert_callbacks = []
        
        # Jamming detection thresholds
        self.signal_drop_threshold = 30  # % drop in signal
        self.interference_threshold = 0.8
        self.packet_loss_threshold = 15  # % packet loss
        
    async def start_monitoring(self):
        """Start continuous jamming detection"""
        self.is_monitoring = True
        print("🛡️ Anti-jamming system activated")
        
        # Start monitoring tasks
        tasks = [
            asyncio.create_task(self.monitor_signal_strength()),
            asyncio.create_task(self.monitor_network_health()),
            asyncio.create_task(self.monitor_interference()),
            asyncio.create_task(self.monitor_gps_jamming())
        ]
        
        await asyncio.gather(*tasks)
    
    async def monitor_signal_strength(self):
        """Monitor WiFi/Cellular signal strength"""
        while self.is_monitoring:
            try:
                # Get WiFi signal strength
                wifi_strength = self.get_wifi_signal_strength()
                
                # Get cellular signal (if available)
                cellular_strength = self.get_cellular_signal_strength()
                
                current_time = time.time()
                signal_data = {
                    'timestamp': current_time,
                    'wifi': wifi_strength,
                    'cellular': cellular_strength
                }
                
                self.signal_strength_history.append(signal_data)
                
                # Keep only last 100 readings
                if len(self.signal_strength_history) > 100:
                    self.signal_strength_history.pop(0)
                
                # Detect sudden signal drops
                if len(self.signal_strength_history) >= 5:
                    await self.analyze_signal_patterns()
                
                await asyncio.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"❌ Signal monitoring error: {e}")
                await asyncio.sleep(5)
    
    def get_wifi_signal_strength(self):
        """Get current WiFi signal strength"""
        try:
            # Linux/Mac command
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            output = result.stdout
            
            # Parse signal strength
            if 'Signal level' in output:
                signal_line = [line for line in output.split('\n') if 'Signal level' in line][0]
                signal_strength = int(signal_line.split('Signal level=')[1].split(' ')[0])
                return abs(signal_strength)  # Convert to positive value
            
            return -50  # Default moderate signal
            
        except Exception:
            # Fallback: simulate signal strength based on network connectivity
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                return 45  # Good signal
            except:
                return 80  # Poor signal
    
    def get_cellular_signal_strength(self):
        """Get cellular signal strength (if available)"""
        try:
            # This would integrate with cellular modem APIs
            # For now, simulate based on system connectivity
            return 60  # Moderate cellular signal
        except:
            return None
    
    async def monitor_network_health(self):
        """Monitor network connectivity and packet loss"""
        while self.is_monitoring:
            try:
                # Test connectivity to multiple servers
                test_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
                connectivity_results = []
                
                for server in test_servers:
                    start_time = time.time()
                    try:
                        socket.create_connection((server, 53), timeout=3)
                        response_time = (time.time() - start_time) * 1000
                        connectivity_results.append({
                            'server': server,
                            'connected': True,
                            'response_time': response_time
                        })
                    except:
                        connectivity_results.append({
                            'server': server,
                            'connected': False,
                            'response_time': None
                        })
                
                # Calculate packet loss percentage
                connected_count = sum(1 for result in connectivity_results if result['connected'])
                packet_loss = ((len(test_servers) - connected_count) / len(test_servers)) * 100
                
                self.network_health = {
                    'timestamp': time.time(),
                    'packet_loss': packet_loss,
                    'connectivity_results': connectivity_results,
                    'avg_response_time': np.mean([r['response_time'] for r in connectivity_results if r['response_time']])
                }
                
                # Detect network jamming
                if packet_loss > self.packet_loss_threshold:
                    await self.handle_potential_jamming('network', {
                        'packet_loss': packet_loss,
                        'threshold': self.packet_loss_threshold
                    })
                
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"❌ Network monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def monitor_interference(self):
        """Monitor RF interference patterns"""
        while self.is_monitoring:
            try:
                # Simulate RF spectrum analysis
                # In real implementation, this would use SDR hardware
                interference_level = self.detect_rf_interference()
                
                if interference_level > self.interference_threshold:
                    await self.handle_potential_jamming('rf_interference', {
                        'interference_level': interference_level,
                        'threshold': self.interference_threshold
                    })
                
                await asyncio.sleep(3)
                
            except Exception as e:
                print(f"❌ Interference monitoring error: {e}")
                await asyncio.sleep(5)
    
    def detect_rf_interference(self):
        """Detect RF interference (simulated)"""
        # In real implementation, this would use SDR to analyze spectrum
        # For now, simulate based on signal strength variations
        
        if len(self.signal_strength_history) < 10:
            return 0.1
        
        recent_signals = [s['wifi'] for s in self.signal_strength_history[-10:] if s['wifi']]
        if not recent_signals:
            return 0.5
        
        # Calculate signal variance (high variance = potential interference)
        signal_variance = np.var(recent_signals)
        interference_level = min(signal_variance / 100, 1.0)
        
        return interference_level
    
    async def monitor_gps_jamming(self):
        """Monitor GPS jamming attempts"""
        while self.is_monitoring:
            try:
                # Check GPS signal availability and accuracy
                gps_status = self.check_gps_health()
                
                if not gps_status['available'] or gps_status['accuracy'] > 50:
                    await self.handle_potential_jamming('gps', gps_status)
                
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"❌ GPS monitoring error: {e}")
                await asyncio.sleep(15)
    
    def check_gps_health(self):
        """Check GPS signal health"""
        # Simulate GPS health check
        # In real implementation, this would interface with GPS hardware
        return {
            'available': True,
            'accuracy': 5.0,  # meters
            'satellites': 8,
            'signal_strength': 'good'
        }
    
    async def analyze_signal_patterns(self):
        """Analyze signal patterns for jamming detection"""
        if len(self.signal_strength_history) < 5:
            return
        
        recent_signals = self.signal_strength_history[-5:]
        older_signals = self.signal_strength_history[-10:-5] if len(self.signal_strength_history) >= 10 else []
        
        if not older_signals:
            return
        
        # Calculate signal strength changes
        recent_avg = np.mean([s['wifi'] for s in recent_signals if s['wifi']])
        older_avg = np.mean([s['wifi'] for s in older_signals if s['wifi']])
        
        signal_drop_percent = ((older_avg - recent_avg) / older_avg) * 100
        
        # Detect sudden signal drops (potential jamming)
        if signal_drop_percent > self.signal_drop_threshold:
            await self.handle_potential_jamming('signal_drop', {
                'drop_percent': signal_drop_percent,
                'recent_avg': recent_avg,
                'older_avg': older_avg
            })
    
    async def handle_potential_jamming(self, jamming_type, details):
        """Handle detected jamming attempt"""
        if not self.jamming_detected:
            self.jamming_detected = True
            
            jamming_event = {
                'type': jamming_type,
                'timestamp': datetime.now().isoformat(),
                'details': details,
                'severity': self.calculate_jamming_severity(jamming_type, details)
            }
            
            print(f"🚨 JAMMING DETECTED: {jamming_type}")
            print(f"📊 Details: {details}")
            
            # Trigger countermeasures
            await self.activate_countermeasures(jamming_event)
            
            # Notify all registered callbacks
            for callback in self.alert_callbacks:
                try:
                    await callback(jamming_event)
                except Exception as e:
                    print(f"❌ Alert callback error: {e}")
            
            # Reset detection flag after cooldown
            await asyncio.sleep(30)
            self.jamming_detected = False
    
    def calculate_jamming_severity(self, jamming_type, details):
        """Calculate jamming severity level"""
        severity_scores = {
            'signal_drop': details.get('drop_percent', 0) / 10,
            'network': details.get('packet_loss', 0) / 5,
            'rf_interference': details.get('interference_level', 0) * 100,
            'gps': 80 if not details.get('available', True) else 20
        }
        
        score = severity_scores.get(jamming_type, 50)
        
        if score >= 80:
            return 'CRITICAL'
        elif score >= 60:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    async def activate_countermeasures(self, jamming_event):
        """Activate anti-jamming countermeasures"""
        print("🛡️ Activating countermeasures...")
        
        countermeasures = []
        
        # Switch to backup communication channel
        if jamming_event['type'] in ['signal_drop', 'network']:
            backup_channel = await self.switch_to_backup_channel()
            countermeasures.append(f"Switched to {backup_channel}")
        
        # Increase transmission power (if possible)
        if jamming_event['type'] == 'rf_interference':
            countermeasures.append("Increased transmission power")
        
        # Enable frequency hopping
        if jamming_event['severity'] in ['HIGH', 'CRITICAL']:
            await self.enable_frequency_hopping()
            countermeasures.append("Enabled frequency hopping")
        
        # Store evidence
        await self.store_jamming_evidence(jamming_event)
        countermeasures.append("Evidence stored")
        
        print(f"✅ Countermeasures activated: {', '.join(countermeasures)}")
    
    async def switch_to_backup_channel(self):
        """Switch to backup communication channel"""
        available_channels = []
        
        # Test each backup channel
        for channel in self.backup_channels:
            if channel != self.current_channel:
                if await self.test_channel_connectivity(channel):
                    available_channels.append(channel)
        
        if available_channels:
            self.current_channel = available_channels[0]
            print(f"📡 Switched to backup channel: {self.current_channel}")
            return self.current_channel
        else:
            print("❌ No backup channels available")
            return self.current_channel
    
    async def test_channel_connectivity(self, channel):
        """Test connectivity on specific channel"""
        # Simulate channel testing
        # In real implementation, this would test actual network interfaces
        await asyncio.sleep(1)
        return True  # Assume backup channels are available
    
    async def enable_frequency_hopping(self):
        """Enable frequency hopping to avoid jamming"""
        print("🔄 Enabling frequency hopping protocol")
        # In real implementation, this would configure radio hardware
        # to rapidly switch between different frequencies
    
    async def store_jamming_evidence(self, jamming_event):
        """Store jamming evidence for analysis"""
        evidence = {
            'event': jamming_event,
            'signal_history': self.signal_strength_history[-20:],  # Last 20 readings
            'network_health': self.network_health,
            'system_state': {
                'cpu_usage': psutil.cpu_percent(),
                'memory_usage': psutil.virtual_memory().percent,
                'network_io': dict(psutil.net_io_counters()._asdict())
            }
        }
        
        # Save to file
        filename = f"jamming_evidence_{int(time.time())}.json"
        with open(f"evidence/{filename}", 'w') as f:
            json.dump(evidence, f, indent=2)
        
        print(f"📁 Evidence stored: {filename}")
    
    def register_alert_callback(self, callback):
        """Register callback for jamming alerts"""
        self.alert_callbacks.append(callback)
    
    def get_system_status(self):
        """Get current anti-jamming system status"""
        return {
            'monitoring': self.is_monitoring,
            'jamming_detected': self.jamming_detected,
            'current_channel': self.current_channel,
            'signal_strength': self.signal_strength_history[-1] if self.signal_strength_history else None,
            'network_health': self.network_health,
            'last_update': datetime.now().isoformat()
        }

# Global anti-jamming system
anti_jamming_system = AntiJammingSystem()
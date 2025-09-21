import asyncio
import time
import os
from datetime import datetime
from typing import Dict, List
import json

class DroneFleetManager:
    def __init__(self):
        self.drones = {}
        self.rth_threshold = 20  # Battery percentage for auto RTH
        self.emergency_rth_threshold = 10  # Critical battery level
        self.monitoring = False
        self.alert_callbacks = []
        # Keep references to running tasks (optional, useful for graceful shutdown)
        self._tasks: List[asyncio.Task] = []

    async def start_monitoring(self):
        """Start continuous drone monitoring"""
        if self.monitoring:
            print("Monitoring already running")
            return

        self.monitoring = True
        print("🚁 Drone fleet monitoring started")

        # Create background tasks and keep references so we can cancel on shutdown
        try:
            battery_task = asyncio.create_task(self.monitor_battery_levels(), name="battery-monitor")
            health_task = asyncio.create_task(self.monitor_drone_health(), name="health-monitor")
            pos_task = asyncio.create_task(self.update_drone_positions(), name="position-updater")

            self._tasks = [battery_task, health_task, pos_task]

            # Wait until tasks finish (they typically run forever until cancelled)
            await asyncio.gather(*self._tasks)
        except asyncio.CancelledError:
            print("start_monitoring cancelled; cancelling child tasks...")
            for t in self._tasks:
                t.cancel()
            raise
        except Exception as e:
            print(f"❌ start_monitoring crashed: {e}")
        finally:
            self.monitoring = False
            self._tasks = []

    async def monitor_battery_levels(self):
        """Monitor all drone battery levels"""
        while self.monitoring:
            try:
                # Iterate over a snapshot of items to avoid RuntimeError if dict changes
                for drone_id, drone in list(self.drones.items()):
                    try:
                        status = drone.get('status')
                        battery = drone.get('battery')
                        if status == 'active' and isinstance(battery, (int, float)):
                            # Emergency RTH - Critical battery
                            if battery <= self.emergency_rth_threshold:
                                # ensure we await to sequence emergency flow
                                await self.emergency_rth(drone_id, battery)

                            # Auto RTH - Low battery
                            elif battery <= self.rth_threshold and not drone.get('returning_home', False):
                                await self.auto_rth(drone_id, battery)

                            # Simulate battery drain during flight (if active and not returning)
                            if status == 'active' and not drone.get('returning_home', False):
                                # update by small float
                                self.drones[drone_id]['battery'] = max(0.0, float(battery) - 0.5)

                        # Simulate battery charging when landed
                        elif status == 'landed':
                            if isinstance(battery, (int, float)) and battery < 100:
                                self.drones[drone_id]['battery'] = min(100.0, float(battery) + 2.0)
                    except Exception as sub_e:
                        print(f"❌ Error handling drone {drone_id} in battery monitor: {sub_e}")

                await asyncio.sleep(10)  # Check every 10 seconds

            except Exception as e:
                print(f"❌ Battery monitoring error: {e}")
                await asyncio.sleep(5)

    async def monitor_drone_health(self):
        """Simple health monitor (placeholder). Can be expanded with real checks"""
        while self.monitoring:
            try:
                # example: check connectivity / heartbeat / sensor health
                for drone_id, drone in list(self.drones.items()):
                    # placeholder health check: ensure required keys exist
                    if 'battery' not in drone:
                        print(f"⚠️ Drone {drone_id} missing battery field")
                    # add other health checks as needed...
                await asyncio.sleep(15)  # health-check interval
            except asyncio.CancelledError:
                print("monitor_drone_health cancelled")
                raise
            except Exception as e:
                print(f"❌ Drone health monitor error: {e}")
                await asyncio.sleep(5)

    async def update_drone_positions(self):
        """Periodic update of drone positions (placeholder / simulation)"""
        while self.monitoring:
            try:
                # This is a light-weight simulation/update loop; in real world you'd read telemetry
                # For now, optionally jitter positions slightly for demo purposes
                for drone_id, drone in list(self.drones.items()):
                    try:
                        if drone.get('status') == 'active' and not drone.get('returning_home', False):
                            # tiny random jitter so map shows movement (non-blocking)
                            # keep deterministic minimal change to avoid too much drift
                            lat = drone.get('lat', 0.0)
                            lon = drone.get('lon', 0.0)
                            # very small incremental move (no random import to keep deterministic)
                            self.drones[drone_id]['lat'] = lat + 0.00001
                            self.drones[drone_id]['lon'] = lon - 0.00001
                    except Exception as sub_e:
                        print(f"❌ Position update error for {drone_id}: {sub_e}")
                await asyncio.sleep(5)  # position update interval
            except asyncio.CancelledError:
                print("update_drone_positions cancelled")
                raise
            except Exception as e:
                print(f"❌ Position updater error: {e}")
                await asyncio.sleep(5)

    async def auto_rth(self, drone_id: str, battery_level: float):
        """Initiate automatic return to home"""
        try:
            print(f"🔋 AUTO RTH TRIGGERED: {drone_id} - Battery: {battery_level}%")

            # Defensive: ensure drone exists
            if drone_id not in self.drones:
                print(f"❌ auto_rth: unknown drone {drone_id}")
                return

            # Update drone status
            self.drones[drone_id].update({
                'returning_home': True,
                'rth_reason': 'low_battery',
                'rth_initiated': datetime.now().isoformat(),
                'status': 'returning'
            })

            # Calculate return path and time
            return_info = await self.calculate_return_path(drone_id)

            # Send RTH command to drone (fire-and-forget simulation)
            await self.send_rth_command(drone_id, return_info)

            # Notify operators
            alert_data = {
                'type': 'auto_rth',
                'drone_id': drone_id,
                'battery_level': battery_level,
                'estimated_return_time': return_info.get('eta'),
                'severity': 'MEDIUM',
                'timestamp': datetime.now().isoformat()
            }

            await self.notify_operators(alert_data)
        except Exception as e:
            print(f"❌ auto_rth error for {drone_id}: {e}")

    async def emergency_rth(self, drone_id: str, battery_level: float):
        """Emergency return to home - critical battery"""
        try:
            print(f"🚨 EMERGENCY RTH: {drone_id} - CRITICAL BATTERY: {battery_level}%")

            if drone_id not in self.drones:
                print(f"❌ emergency_rth: unknown drone {drone_id}")
                return

            # Update drone status
            self.drones[drone_id].update({
                'returning_home': True,
                'rth_reason': 'critical_battery',
                'rth_initiated': datetime.now().isoformat(),
                'emergency_mode': True,
                'status': 'returning'
            })

            # Calculate fastest return path
            return_info = await self.calculate_emergency_return(drone_id)

            # Send emergency RTH command
            await self.send_emergency_rth_command(drone_id, return_info)

            # High priority alert
            alert_data = {
                'type': 'emergency_rth',
                'drone_id': drone_id,
                'battery_level': battery_level,
                'estimated_return_time': return_info.get('eta'),
                'severity': 'CRITICAL',
                'timestamp': datetime.now().isoformat()
            }

            await self.notify_operators(alert_data)
        except Exception as e:
            print(f"❌ emergency_rth error for {drone_id}: {e}")

    async def calculate_return_path(self, drone_id: str):
        """Calculate optimal return path"""
        drone = self.drones.get(drone_id)
        if not drone:
            return {'distance': 0, 'eta': 0, 'path': [], 'home_base': {'lat': 0, 'lon': 0}}

        home_base = {'lat': 28.7041, 'lon': 77.1025}  # Base coordinates

        # Calculate distance to home (meters)
        distance = self.calculate_distance(
            float(drone.get('lat', 0.0)), float(drone.get('lon', 0.0)),
            home_base['lat'], home_base['lon']
        )

        # Estimate return time (assuming 15 m/s speed)
        # Ensure speed > 0
        speed_m_s = 15.0
        eta_seconds = distance / speed_m_s if speed_m_s > 0 else 0.0

        return {
            'distance': distance,
            'eta': eta_seconds,
            'path': [
                {'lat': drone.get('lat'), 'lon': drone.get('lon')},
                {'lat': home_base['lat'], 'lon': home_base['lon']}
            ],
            'home_base': home_base
        }

    async def calculate_emergency_return(self, drone_id: str):
        """Calculate fastest emergency return path"""
        return_info = await self.calculate_return_path(drone_id)
        # Reduce ETA by 30% for emergency speed
        try:
            return_info['eta'] = float(return_info.get('eta', 0.0)) * 0.7
            return_info['emergency_speed'] = True
        except Exception:
            pass
        return return_info

    async def send_rth_command(self, drone_id: str, return_info: dict):
        """Send RTH command to drone"""
        print(f"📡 Sending RTH command to {drone_id}")

        # In real implementation, this would send actual commands to drone
        # For now, simulate the return journey as a background task
        # Use create_task so this function returns immediately
        try:
            asyncio.create_task(self.simulate_return_journey(drone_id, return_info))
        except Exception as e:
            print(f"❌ Failed to create simulate_return_journey task for {drone_id}: {e}")

    async def send_emergency_rth_command(self, drone_id: str, return_info: dict):
        """Send emergency RTH command"""
        print(f"🚨 Sending EMERGENCY RTH command to {drone_id}")

        try:
            asyncio.create_task(self.simulate_emergency_return_journey(drone_id, return_info))
        except Exception as e:
            print(f"❌ Failed to create simulate_emergency_return_journey task for {drone_id}: {e}")

    async def simulate_return_journey(self, drone_id: str, return_info: dict):
        """Simulate drone returning home"""
        drone = self.drones.get(drone_id)
        if not drone:
            print(f"❌ simulate_return_journey: unknown drone {drone_id}")
            return

        home_base = return_info.get('home_base', {'lat': 28.7041, 'lon': 77.1025})
        total_time = float(return_info.get('eta', 0.0))

        print(f"🏠 {drone_id} returning home - ETA: {total_time:.1f}s")

        # Protect against zero ETA
        steps = 10
        sleep_per_step = (total_time / steps) if total_time > 0 else 0.5

        for step in range(steps + 1):
            progress = step / steps

            # Interpolate position
            current_lat = float(drone.get('lat', home_base['lat'])) + (home_base['lat'] - float(drone.get('lat', home_base['lat']))) * progress
            current_lon = float(drone.get('lon', home_base['lon'])) + (home_base['lon'] - float(drone.get('lon', home_base['lon']))) * progress
            current_alt = max(0, float(drone.get('alt', 50.0)) * (1 - progress))  # Descend gradually

            # Update drone position
            self.drones[drone_id].update({
                'lat': current_lat,
                'lon': current_lon,
                'alt': current_alt
            })

            # reduce battery a bit while returning
            if isinstance(self.drones[drone_id].get('battery'), (int, float)):
                self.drones[drone_id]['battery'] = max(0.0, float(self.drones[drone_id]['battery']) - (0.5 * (1 + progress)))

            await asyncio.sleep(sleep_per_step)

        # Drone has landed
        await self.land_drone(drone_id)

    async def simulate_emergency_return_journey(self, drone_id: str, return_info: dict):
        """Simulate emergency return journey"""
        print(f"🚨 {drone_id} EMERGENCY RETURN in progress")
        await self.simulate_return_journey(drone_id, return_info)
        await self.emergency_landing_procedures(drone_id)

    async def land_drone(self, drone_id: str):
        """Land drone at home base"""
        print(f"🛬 {drone_id} landing at home base")

        if drone_id not in self.drones:
            print(f"❌ land_drone: unknown drone {drone_id}")
            return

        self.drones[drone_id].update({
            'status': 'landed',
            'returning_home': False,
            'emergency_mode': False,
            'lat': 28.7041,  # Home base coordinates
            'lon': 77.1025,
            'alt': 0,
            'landed_at': datetime.now().isoformat()
        })

        # Notify successful landing
        alert_data = {
            'type': 'drone_landed',
            'drone_id': drone_id,
            'battery_level': self.drones[drone_id].get('battery'),
            'landing_reason': self.drones[drone_id].get('rth_reason', 'manual'),
            'timestamp': datetime.now().isoformat()
        }

        await self.notify_operators(alert_data)

    async def emergency_landing_procedures(self, drone_id: str):
        """Execute emergency landing procedures"""
        print(f"🚨 Emergency landing procedures for {drone_id}")

        if drone_id not in self.drones:
            print(f"❌ emergency_landing_procedures: unknown drone {drone_id}")
            return

        # Ensure logs directory exists
        logs_dir = "logs"
        try:
            os.makedirs(logs_dir, exist_ok=True)
        except Exception as e:
            print(f"❌ Could not create logs directory '{logs_dir}': {e}")

        # Log emergency event
        emergency_log = {
            'drone_id': drone_id,
            'event': 'emergency_landing',
            'battery_level': self.drones[drone_id].get('battery'),
            'timestamp': datetime.now().isoformat(),
            'location': {
                'lat': self.drones[drone_id].get('lat'),
                'lon': self.drones[drone_id].get('lon')
            }
        }

        try:
            filename = os.path.join(logs_dir, f"emergency_{drone_id}_{int(time.time())}.json")
            with open(filename, 'w') as f:
                json.dump(emergency_log, f, indent=2)
        except Exception as e:
            print(f"❌ Failed to write emergency log for {drone_id}: {e}")

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates (in meters)"""
        import math

        R = 6371000  # Earth's radius in meters
        lat1_rad = math.radians(float(lat1))
        lat2_rad = math.radians(float(lat2))
        delta_lat = math.radians(float(lat2) - float(lat1))
        delta_lon = math.radians(float(lon2) - float(lon1))

        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon/2) * math.sin(delta_lon/2))

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c

        return distance

    async def notify_operators(self, alert_data: dict):
        """Notify operators about drone events"""
        try:
            print(f"📢 ALERT: {alert_data}")

            # Send to all registered callbacks (assume callbacks are async)
            for callback in list(self.alert_callbacks):
                try:
                    maybe_coro = callback(alert_data)
                    if asyncio.iscoroutine(maybe_coro):
                        await maybe_coro
                    # if callback is sync, it will have already executed
                except Exception as e:
                    print(f"❌ Alert callback error: {e}")
        except Exception as e:
            print(f"❌ notify_operators error: {e}")

    def register_alert_callback(self, callback):
        """Register callback for drone alerts"""
        self.alert_callbacks.append(callback)

    def add_drone(self, drone_data: dict):
        """Add drone to fleet"""
        drone_id = drone_data.get('drone_id')
        if not drone_id:
            raise ValueError("drone_data must contain 'drone_id'")
        self.drones[drone_id] = drone_data

    def get_fleet_status(self):
        """Get current fleet status"""
        return {
            'total_drones': len(self.drones),
            'active_drones': len([d for d in self.drones.values() if d.get('status') == 'active']),
            'returning_drones': len([d for d in self.drones.values() if d.get('returning_home', False)]),
            'low_battery_drones': len([d for d in self.drones.values() if isinstance(d.get('battery'), (int, float)) and d.get('battery') <= self.rth_threshold]),
            'drones': self.drones,
            'monitoring': self.monitoring
        }

    async def manual_rth(self, drone_id: str):
        """Manual return to home command"""
        if drone_id in self.drones:
            await self.auto_rth(drone_id, self.drones[drone_id].get('battery', 0))
            return True
        return False

    async def emergency_rth_all(self):
        """Emergency RTH for all active drones"""
        print("🚨 EMERGENCY RTH - ALL DRONES")

        active_drones = [drone_id for drone_id, drone in self.drones.items()
                         if drone.get('status') == 'active']

        # Launch emergency RTHs concurrently but don't block each other
        coros = []
        for drone_id in active_drones:
            coros.append(self.emergency_rth(drone_id, self.drones[drone_id].get('battery', 0)))

        if coros:
            # run all concurrently
            await asyncio.gather(*coros, return_exceptions=True)

# Global drone fleet manager
drone_fleet = DroneFleetManager()

# Initialize with sample drones
sample_drones = {
    "GUARD-01": {"drone_id": "GUARD-01", "lat": 28.7041, "lon": 77.1025, "alt": 120.4, "battery": 78, "status": "active", "detection": "Clear", "confidence": 0.0},
    "GUARD-02": {"drone_id": "GUARD-02", "lat": 28.7055, "lon": 77.1100, "alt": 95.1, "battery": 25, "status": "active", "detection": "Human", "confidence": 0.85},
    "GUARD-03": {"drone_id": "GUARD-03", "lat": 28.7000, "lon": 77.1000, "alt": 140.0, "battery": 15, "status": "active", "detection": "Clear", "confidence": 0.0},
    "GUARD-04": {"drone_id": "GUARD-04", "lat": 28.7020, "lon": 77.0950, "alt": 80.0, "battery": 91, "status": "active", "detection": "Human", "confidence": 0.92}
}

for drone_data in sample_drones.values():
    drone_fleet.add_drone(drone_data)

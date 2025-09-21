@app.post("/api/mobile/alert")
async def mobile_alert_endpoint():
    """Mobile app integration"""
    return {
        'push_notifications': True,
        'real_time_updates': True,
        'offline_capability': True
    }

@app.get("/api/mobile/dashboard")
async def mobile_dashboard():
    """Mobile dashboard data"""
    return {
        'active_threats': get_active_threats(),
        'patrol_status': get_patrol_status(),
        'system_health': get_system_health(),
        'quick_actions': get_quick_actions()
    }
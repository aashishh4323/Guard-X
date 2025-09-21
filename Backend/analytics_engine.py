import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3

class AnalyticsEngine:
    def __init__(self):
        self.db_path = "surveillance_analytics.db"
        self.init_database()
        
    def init_database(self):
        """Initialize analytics database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME,
                location TEXT,
                threat_type TEXT,
                confidence REAL,
                operator TEXT,
                resolved BOOLEAN
            )
        ''')
        conn.close()
    
    def generate_threat_trends(self, days=30):
        """Generate threat trend analysis"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(f'''
            SELECT DATE(timestamp) as date, 
                   COUNT(*) as incidents,
                   AVG(confidence) as avg_confidence
            FROM detections 
            WHERE timestamp >= datetime('now', '-{days} days')
            GROUP BY DATE(timestamp)
        ''', conn)
        
        # Create interactive plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['incidents'],
            mode='lines+markers',
            name='Daily Incidents'
        ))
        
        return fig.to_html()
    
    def get_performance_metrics(self):
        """System performance dashboard"""
        return {
            'total_detections': self.get_total_detections(),
            'accuracy_rate': self.calculate_accuracy(),
            'response_time': self.avg_response_time(),
            'false_positive_rate': self.calculate_false_positives(),
            'system_uptime': self.get_uptime()
        }
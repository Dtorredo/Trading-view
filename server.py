import http.server
import socketserver
import json
import urllib.parse
import os
import sys

# Import functions from trading_dashboard
import trading_dashboard

PORT = 9090

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence default request logging to keep console clean
        pass

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def serve_file(self, filepath, content_type='text/html'):
        if os.path.exists(filepath):
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, f"File not found: {filepath}")

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == '/' or path == '/index.html':
            self.serve_file('index.html')
        elif path == '/sizer':
            self.serve_file('sizer.html')
        elif path == '/journal':
            self.serve_file('journal.html')
        elif path == '/roadmap':
            self.serve_file('roadmap.html')
        elif path == '/api/stats':
            # Run NumPy based stats analysis
            stats_all = trading_dashboard.analyse_trades("all")
            stats_today = trading_dashboard.analyse_trades("today")
            
            # Extract raw trade history
            trades = trading_dashboard.load_trades()
            
            # Format and respond
            self.send_json({
                "all": stats_all if stats_all else {"total_trades": 0, "total_pnl": 0.0, "win_rate": 0.0, "equity_curve": [], "patterns": {}},
                "today": stats_today if stats_today else {"total_trades": 0, "total_pnl": 0.0, "win_rate": 0.0, "equity_curve": []},
                "trades": list(reversed(trades))  # Show newest first
            })
        elif path == '/api/projections':
            # Funded income projections calculation (extracted from python broadcasting logic)
            np = trading_dashboard.np
            account_sizes = np.array([10000, 25000, 50000, 100000, 200000])
            monthly_rate = 0.04
            split = 0.80
            gross_monthly = np.round(account_sizes * monthly_rate, 2)
            net_monthly = np.round(gross_monthly * split, 2)
            annual_net = np.round(net_monthly * 12, 2)
            kes_monthly = np.round(net_monthly * 130, 0).astype(int)

            projections = []
            labels = ["$10K account", "$25K account", "$50K account", "$100K account", "$200K AUM fund"]
            for i in range(len(labels)):
                projections.append({
                    "label": labels[i],
                    "size": int(account_sizes[i]),
                    "gross_monthly": float(gross_monthly[i]),
                    "net_monthly": float(net_monthly[i]),
                    "annual_net": float(annual_net[i]),
                    "kes_monthly": int(kes_monthly[i])
                })
            
            self.send_json({
                "projections": projections
            })
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # Read POST body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            params = json.loads(post_data) if post_data else {}
        except Exception:
            params = {}

        if path == '/api/trades/log':
            result = params.get('result', 'win')
            pnl = float(params.get('pnl', 0.0))
            pattern = params.get('pattern', 'CHoCH')
            session = params.get('session', 'London')
            notes = params.get('notes', '')
            asset = params.get('asset', 'XAUUSD')
            direction = params.get('direction', 'Long')
            entry = params.get('entry', 'N/A')
            exit = params.get('exit', 'N/A')
            sl = params.get('sl', 'N/A')
            tp = params.get('tp', 'N/A')

            # Log using NumPy framework logic
            trading_dashboard.log_trade(
                result, pnl, pattern, session, notes,
                asset=asset, direction=direction, entry=entry, exit=exit, sl=sl, tp=tp
            )

            # Check daily limits warning status
            trades = trading_dashboard.load_trades()
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            today_trades = [t for t in trades if t["date"] == today]
            today_losses = [t for t in today_trades if t["result"] == "loss"]
            daily_stop_hit = len(today_losses) >= 2

            self.send_json({
                "status": "success",
                "daily_stop_hit": daily_stop_hit,
                "message": "DAILY STOP HIT — 2 losses today. CLOSE THE PLATFORM." if daily_stop_hit else "Trade logged successfully."
            })

        elif path == '/api/calculate':
            balance = float(params.get('balance', 70.0))
            risk_pct = float(params.get('risk_pct', 2.0))
            sl_points = float(params.get('sl_points', 8.0))
            rr = float(params.get('rr', 2.0))
            instrument = params.get('instrument', 'XAUUSD')

            # Calculate sizer parameters via NumPy logic
            result = trading_dashboard.calculate_position(balance, risk_pct, sl_points, rr, instrument)
            self.send_json(result)

        elif path == '/api/project':
            balance = float(params.get('balance', 70.0))
            rate = float(params.get('rate', 15.0))
            months = int(params.get('months', 36))

            # Run growth projection curve calculation via NumPy logic
            result = trading_dashboard.project_growth(balance, rate, months)
            self.send_json(result)

        else:
            self.send_error(404, "Not Found")

def run():
    # Configure socket server to reuse addresses to prevent port in-use issues on restarts
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"\n🚀 ProTrader Terminal Web Application is running!")
        print(f"🔗 Open your browser at: http://localhost:{PORT}")
        print(f"Press Ctrl+C to terminate.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            sys.exit(0)

if __name__ == '__main__':
    run()

"""NiceGUI theme and styling."""

LIGHT_THEME = {
    "primary": "#2E7D32",
    "secondary": "#1976D2",
    "accent": "#00BCD4",
    "dark": "#1E1E1E",
    "light": "#F5F5F5",
    "error": "#D32F2F",
    "success": "#388E3C",
}

DARK_THEME = {
    "primary": "#66BB6A",
    "secondary": "#42A5F5",
    "accent": "#4DD0E1",
    "dark": "#121212",
    "light": "#E0E0E0",
    "error": "#EF5350",
    "success": "#81C784",
}

CSS_STYLES = """
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    overflow: hidden;
}

.workspace-container {
    display: flex;
    height: 100vh;
    gap: 10px;
    padding: 10px;
}

.sidebar {
    width: 250px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
    padding: 15px;
    color: white;
    overflow-y: auto;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.main-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.content-area {
    flex: 1;
    background: white;
    border-radius: 10px;
    padding: 20px;
    overflow-y: auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.status-bar {
    background: #2d2d2d;
    color: #00ff00;
    padding: 10px 15px;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.agent-status {
    padding: 10px;
    margin: 5px 0;
    background: rgba(255,255,255,0.1);
    border-left: 3px solid #00ff00;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.agent-status.working {
    border-left-color: #ffff00;
}

.agent-status.error {
    border-left-color: #ff0000;
}

.card {
    background: white;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transform: translateY(-2px);
}

.button {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s ease;
}

.button-primary {
    background: #667eea;
    color: white;
}

.button-primary:hover {
    background: #5568d3;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.input {
    padding: 10px;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.3s ease;
}

.input:focus {
    border-color: #667eea;
    outline: none;
}
"""

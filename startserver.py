from app import app
from service import server


server.run(debug=True, port=8000)
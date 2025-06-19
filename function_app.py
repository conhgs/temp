import azure.functions as func
from src.presentation.blueprints import bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
app.register_functions(bp)

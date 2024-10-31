import os


class Config:
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://briankimathi94:PEXpmaDRxHhDhG4D@cluster0.xxnli.mongodb.net/your_database_name?retryWrites=true&w=majority&appName=Cluster0",
    )

from dotenv import load_dotenv, dotenv_values
load_dotenv()
vals = dotenv_values('.env')

BOT_TOKEN = vals['BOT_TOKEN']
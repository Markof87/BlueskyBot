from atproto import Client, models
import requests
import config
import utils
import reports

client = Client()

BSKY_HANDLE = config.BSKY_HANDLE
BSKY_PASSWORD = config.BSKY_PASSWORD

# Auth with Bluesky
try:
    client.login(BSKY_HANDLE, BSKY_PASSWORD)
    print("Autenticazione avvenuta con successo.")
except Exception as e:
    print(f"Errore durante l'autenticazione: {e}")
    exit(1)
    # Open the image, send it to Bluesky

# URL del servizio
#url = 'http://localhost:5000/match/1824918'

event_name = 'Pass'

url = 'https://markof.pythonanywhere.com/match/1821141/player/331924/event/' + event_name

# Fai la richiesta GET per ottenere i dati
response = requests.get(url)

# Assicurati che la richiesta sia andata a buon fine
if response.status_code == 200:
    match_data = response.json()
else:
    print(f"Errore nella richiesta: {response.status_code}")

#events = {"events": match_data}
#events_ls = utils.createEventsDF(events)
name = 'Ugarte'
opponent = 'Nottingham Forest'

img_buffer = reports.getEventReport(match_data, event_name, name, opponent, pitch_color='#FFFFFF')
img_buffer.seek(0)
image_data = utils.compress_image(img_buffer.read(), target_size_kb=976.56, initial_resize_factor=1.0)

with open('debug_image.png', 'wb') as f:
    f.write(image_data)
print("Immagine salvata come debug_image.png per verifica.")

if not image_data:
    print("Errore: Il buffer dell'immagine è vuoto.")
    exit(1)

upload = client.com.atproto.repo.upload_blob(image_data, timeout=120)
embed = models.AppBskyEmbedImages.Main(
    images=[{
        "image": upload.blob,
        "alt": "Pass map visualization"
    }]
)
client.send_post(text='Pass map for the match!', embed=embed)

print("Immagine inviata con successo.")


#client.send_post(text='aaaaa')

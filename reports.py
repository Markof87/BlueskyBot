from io import BytesIO

from mplsoccer.pitch import VerticalPitch
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd


def getEventReport(match_data, event_name, name, opponent, pitch_color):

    font_path = 'resources/fonts/Druk-Wide-Web-Bold-Regular.ttf' 
    custom_font = fm.FontProperties(fname=font_path)

    #Filter events based on the event_name
    events = [event for event in match_data if event['type']["displayName"] == event_name]

    successful_events = pd.DataFrame([e for e in events if e['outcomeType']["displayName"] == 'Successful'])
    unsuccessful_events = pd.DataFrame([e for e in events if e['outcomeType']["displayName"] == 'Unsuccessful'])

    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color=pitch_color, line_color='#4c566a', linewidth=1.5, stripe=False)
    fig, ax = pitch.draw(figsize=(6.5, 10))

    if not successful_events.empty:

        if(event_name == 'Pass'):
            pitch.arrows(successful_events["x"]/100*120, 80-successful_events["y"]/100*80, successful_events["endX"]/100*120, 80-successful_events["endY"]/100*80, width=1.5, headwidth=10, headlength=10, color='#32CD32', ax=ax, alpha=0.6, label="completed")
        else:
            pitch.scatter(successful_events["x"]/100*120, 80-successful_events["y"]/100*80, s=100, color='#32CD32', ax=ax, alpha=0.6, label="completed")

    if not unsuccessful_events.empty:

        if(event_name == 'Pass'):
            pitch.arrows(unsuccessful_events["x"]/100*120, 80-unsuccessful_events["y"]/100*80, unsuccessful_events["endX"]/100*120, 80-unsuccessful_events["endY"]/100*80, width=1.5, headwidth=8, headlength=8, color='#FF0000', ax=ax, alpha=0.6, label="blocked")
        else:
            pitch.scatter(unsuccessful_events["x"]/100*120, 80-unsuccessful_events["y"]/100*80, s=100, color='#FF0000', ax=ax, alpha=0.6, label="uncompleted")

    ax.legend(facecolor=pitch_color, handlelength=5, edgecolor='None', fontsize=8, loc='lower left', shadow=True, labelcolor='black')
    
    # Add title
    fig.text(0.1, 0.95, f'{name} {event_name} vs {opponent}', fontsize=16, color='black', fontweight='bold', fontproperties=custom_font)
    fig.text(0.1, 0.93, 'Data Source: WhoScored/Opta', fontsize=8, color='black', fontstyle='italic', fontproperties=custom_font)
    
    # Set background color
    fig.patch.set_facecolor(pitch_color)

    # Salva l'immagine in memoria
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)  
    plt.close(fig)  

    return img_buffer

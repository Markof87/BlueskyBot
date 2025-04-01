from io import BytesIO

from mplsoccer.pitch import VerticalPitch
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

def getPasses(match_data, name, opponent, pitch_color):
 
    font_path = 'resources/fonts/Druk-Wide-Web-Bold-Regular.ttf' 
    custom_font = fm.FontProperties(fname=font_path)
    # Filter passes
    passes = [event for event in match_data if event['type']["displayName"] == 'Pass']
    
    successful_passes = [p for p in passes if p['outcomeType']["displayName"] == 'Successful']
    unsuccessful_passes = [p for p in passes if p['outcomeType']["displayName"] == 'Unsuccessful']
    
    # Setup the pitch with a dark background
    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color=pitch_color, line_color='#4c566a', 
                  linewidth=1.5, stripe=False)
    fig, ax = pitch.draw(figsize=(6.5, 10))

    successful_passes = pd.DataFrame(successful_passes)
    unsuccessful_passes = pd.DataFrame(unsuccessful_passes)    
    # Plot successful passes with a vibrant color
    pitch.arrows(successful_passes["x"]/100*120, 80-successful_passes["y"]/100*80,
                 successful_passes["endX"]/100*120, 80-successful_passes["endY"]/100*80,
                 width=1.5, headwidth=10, headlength=10, color='#32CD32', ax=ax, alpha=0.6, label="completed")
    
    # Plot unsuccessful passes with a faded color
    pitch.arrows(unsuccessful_passes["x"]/100*120, 80-unsuccessful_passes["y"]/100*80,
                 unsuccessful_passes["endX"]/100*120, 80-unsuccessful_passes["endY"]/100*80,
                 width=1.5, headwidth=8, headlength=8, color='#FF0000', ax=ax, alpha=0.6, label="blocked")
    
    ax.legend(facecolor=pitch_color, handlelength=5, edgecolor='None', fontsize=8, loc='lower left', shadow=True, labelcolor='black')
    
    # Add title
    fig.text(0.1, 0.95, f'{name} Passes vs {opponent}', fontsize=16, color='black', fontweight='bold', fontproperties=custom_font)
    fig.text(0.1, 0.93, 'Data Source: WhoScored/Opta', fontsize=10, color='black', fontstyle='italic', fontproperties=custom_font)

    orientation_arrow = FancyArrowPatch((-3, 40), (-3, 80), arrowstyle='-|>', color='black', lw=2, mutation_scale=20)
    ax.add_patch(orientation_arrow)
    
    # Set background color
    fig.patch.set_facecolor(pitch_color)
    #plt.savefig("match_pass_map.png", dpi=300, bbox_inches='tight')

    #plt.show()

    # Salva l'immagine in memoria
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)  # Torna all'inizio del buffer
    plt.close(fig)  # Chiudi la figura per liberare memoria

    return img_buffer

def getBallRecovery(match_data, team, opponent, pitch_color):
 
    font_path = 'resources/fonts/Druk-Wide-Web-Bold-Regular.ttf' 
    custom_font = fm.FontProperties(fname=font_path)
    # Filter passes
    ball_recoveries = [event for event in match_data if event['type']["displayName"] == 'BallRecovery']
    
    successful_recoveries = [p for p in ball_recoveries if p['outcomeType']["displayName"] == 'Successful']
    unsuccessful_recoveries = [p for p in ball_recoveries if p['outcomeType']["displayName"] == 'Unsuccessful']
    
    # Setup the pitch with a dark background
    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color=pitch_color, line_color='#4c566a', 
                  linewidth=1.5, stripe=False)
    fig, ax = pitch.draw(figsize=(6.5, 10))

    successful_recoveries = pd.DataFrame(successful_recoveries)
    unsuccessful_recoveries = pd.DataFrame(unsuccessful_recoveries)    

    if not successful_recoveries.empty:    
        pitch.scatter(successful_recoveries["x"]/100*120, 80-successful_recoveries["y"]/100*80, s=100, color='#32CD32', ax=ax, alpha=0.6, label="completed")
    if not unsuccessful_recoveries.empty:
        pitch.scatter(unsuccessful_recoveries["x"]/100*120, 80-unsuccessful_recoveries["y"]/100*80, s=100, color='#FF0000', ax=ax, alpha=0.6, label="blocked")

    ax.legend(facecolor=pitch_color, handlelength=5, edgecolor='None', fontsize=8, loc='lower left', shadow=True, labelcolor='black')
    
    # Add title
    fig.text(0.1, 0.95, f'{team} Passes vs {opponent}', fontsize=16, color='black', fontweight='bold', fontproperties=custom_font)
    fig.text(0.1, 0.93, 'Data Source: WhoScored/Opta', fontsize=10, color='black', fontstyle='italic', fontproperties=custom_font)
    
    # Set background color
    fig.patch.set_facecolor(pitch_color)
    #plt.savefig("match_pass_map.png", dpi=300, bbox_inches='tight')

    #plt.show()

    # Salva l'immagine in memoria
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)  # Torna all'inizio del buffer
    plt.close(fig)  # Chiudi la figura per liberare memoria

    return img_buffer


import seaborn as sns
from datetime import datetime
import re

def set_seaborn_style(font_family, background_color, grid_color, text_color):
    sns.set_style({
        "axes.facecolor": background_color,
        "figure.facecolor": background_color,

        "grid.color": grid_color,
        "axes.edgecolor": grid_color,
        "axes.grid": True,
        "axes.axisbelow": True,
        
        "axes.labelcolor": text_color,
        "text.color": text_color,
        "font.family": font_family,
        "xtick.color": text_color,
        "ytick.color": text_color,

        "xtick.bottom": False,
        "xtick.top": False,
        "ytick.left": False,
        "ytick.right": False,

        "axes.spines.left": False,
        "axes.spines.bottom": True,
        "axes.spines.right": False,
        "axes.spines.top": False,
    })


def days_between_dates(date_str1, date_str2):
    # Convert date strings to datetime objects
    date_format = "%A, %b %d, %Y %H:%M"
    datetime1 = datetime.strptime(date_str1, date_format)
    datetime2 = datetime.strptime(date_str2, date_format)

    # Calculate the number of days between
    time_difference = datetime2 - datetime1
    days_between = abs(time_difference.days)

    return days_between
def is_reaction(text):
    reactions = ['Laughed at', 'Loved', 'Emphasized', 'Questioned', 'Disliked']
    
    patterns = []
    for reacted_to in reactions:
        patterns.append( re.compile(fr'{reacted_to} an image') )
        patterns.append( re.compile(fr'{reacted_to} a movie') )
        patterns.append( re.compile(fr'{reacted_to} “.*”') )

    for pattern in patterns:
        if pattern.match(text):
            return True

    return False


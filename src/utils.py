import seaborn as sns
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from afinn import Afinn
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


def get_positive_adjectives(text):
    afn = Afinn()
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    adjectives = [word for word, pos in pos_tags if pos.startswith('JJ')]
    positive_adjectives = [adj for adj in adjectives if afn.score(adj) > 0]
    return positive_adjectives


def create_custom_colormap(colors):
    custom_cmap = LinearSegmentedColormap.from_list("custom_colormap", colors, N=256)
    return custom_cmap


def generate_wordcloud(text, mask_image_path, colors):
    # Create word cloud with image mask
    mask_image = np.array(Image.open(mask_image_path))
    cloud_colors = ImageColorGenerator(mask_image)
    wordcloud = WordCloud(width=800, height=400, mask=mask_image)
    wordcloud.generate(text)

    # Plot the word cloud
    plt.figure(figsize=(30, 30))
    cmap = create_custom_colormap(colors)
    plt.imshow(wordcloud.recolor(colormap=cmap), interpolation='bilinear')
    plt.axis("off")
    plt.show()


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


def get_reaction_type(reaction_text):
    words = reaction_text.split()
    if words:
        return words[0]
    else:
        return None
    

def get_sentiment_score(text):
    afn = Afinn()
    return afn.score(text)
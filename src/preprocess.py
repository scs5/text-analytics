import pandas as pd
import re
import emoji

RAW_DATA_FN = './data/texts.csv'
CLEANED_DATA_FN = './data/cleaned_texts.csv'
PHONE_NUMBER_DICT = {'+19999999999': 'Sam', 
                     '+18888888888': 'Taylor'}


def clean_sender(row):
    """ Clean sender (correct name and remove phone number). """
    # Find phone number
    full_sender = row['Sender']
    phone = re.findall(r'\((.*?)\)', full_sender)[0]
    
    # Replace with correct sender name
    sender_name = PHONE_NUMBER_DICT[phone]
    return sender_name


def count_emojis(text, emojis):
    count = 0
    for emoji_str in emojis:
        count += str(text).count(emoji_str)
    return count


def preprocess(df):
    # Clean sender
    df['Sender'] = df.apply(clean_sender, axis=1)

    # Remove unwanted columns
    df = df.drop(columns=['Received', 'iMessage'])

    # Add word length
    df['num_words'] = [len(str(msg).split()) for msg in df['Text']]

    # Convert emojis to unicode
    df['Text'] = [emoji.demojize(str(msg)) for msg in df['Text']]

    # Number of emojis
    special_emojis = [':)', ':/', ':(', '◡̈']
    emojis = special_emojis + [em['en'] for em in emoji.EMOJI_DATA.values()]
    df['emoji_num'] = df['Text'].apply(lambda x: count_emojis(x, emojis=emojis))

    # Save cleaned data
    df.to_csv(CLEANED_DATA_FN, index=False)

    return df


if __name__ == '__main__':
    df = pd.read_csv(RAW_DATA_FN)
    df = preprocess(df)
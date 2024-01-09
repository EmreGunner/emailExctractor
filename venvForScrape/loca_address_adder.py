import pandas as pd
import os
import re

#df = pd.read_csv("/inputs/gmaps_output.csv")
#path = os.path.join(os.getcwd(), "/inputs/gmaps_output.csv")
#root_path = os.getcwd() 
#path = os.path.join(root_path, "inputs/gmaps_use_this.csv")
#sokak_count = cadde_count = mah_count = blv_count = unknown_count = nan_count = plz_count = resi_count = ofc_count= 0
#df = pd.read_csv(path)


#sample_df = df[["address"]].head(n=3)
#for index, row in sample_df.iterrows():
#    print(f"{index} {row}")

def extract_backup(address):
    # Regular expressions for different address components
    patterns = {
    'sokagi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (sk\.|sk|sokak|sok\.|sokagi|street)\b',
    'caddesi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (cd\.|cd|cad\.|cad|caddesi)\b',
    'mahallesi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (mh\.|mah\.|mahallesi)\b',
    'bulvari': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (blv\.|blv|bulvar|boulevard)\b',
    'plazasi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (plaza|plz\.|plz)\b',
    'rezidansi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (rezidans|residence)\b',
    'ofisi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (office|ofis)\b'
    }
    # Handle non-existent addresses
    if address is None or pd.isna(address):
        return '' 

    # Ensure the address is a string
    if not isinstance(address, str):
        return '' 

    address_lower = address.lower()

    # Check and extract based on patterns
    for key, pattern in patterns.items():
        match = re.search(pattern, address_lower)
        if match:
            extracted = match.group(1)
            # Special handling for Turkish characters
            extracted = extracted.replace('i', 'İ').replace('ı', 'I').title()
            return f"{extracted} {key}"

    # Return default for unknown addresses
    return ''

def revised_extract(address):
    # Improved regular expressions for different address components
    patterns = {
        'sokagi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (sokak|sok\.|sokagi|street)\b',
        'caddesi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (cadde|cad\.|caddesi)\b',
        'mahallesi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (mahalle|mah\.|mahallesi)\b',
        'bulvari': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (bulvar|blv\.|blv)\b',
        'plazasi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (plaza|plz\.|plz)\b',
        'rezidansi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (rezidans|residence)\b',
        'ofisi': r'([A-Za-zÇŞĞÜÖİçşğüöı]+(?: [A-Za-zÇŞĞÜÖİçşğüöı]+)*?) (office|ofis)\b'
    }

    # Handle non-existent addresses
    if address is None or pd.isna(address):
        return '' 

    # Ensure the address is a string and convert to lowercase
    if not isinstance(address, str):
        return '' 
    address_lower = address.lower()

    # Check and extract based on patterns
    for key, pattern in patterns.items():
        match = re.search(pattern, address_lower)
        if match:
            extracted = match.group(1)
            # Special handling for Turkish characters and title case
            extracted = extracted.replace('i', 'İ').replace('ı', 'I').title()
            # Format the result with uppercase first letter for each word
            formatted_extracted = ' '.join(word[0].upper() + word[1:] for word in extracted.split())
            return f"{formatted_extracted} {key.title()}"

    # Return default for unknown addresses
    return ''

def extract(address):
    # Regular expressions for different address components
    patterns = {
        'sokagi': r'([A-Za-zÇŞĞÜÖİçşğüöı\-]+(?: [A-Za-zÇŞĞÜÖİçşğüöı\-]+)*?) (sk\.|sk|sokak|sok\.|sokagi|street)\b',
        'caddesi': r'([A-Za-zÇŞĞÜÖİçşğüöı\-]+(?: [A-Za-zÇŞĞÜÖİçşğüöı\-]+)*?) (cd\.|cd|cad\.|cad|caddesi)\b',
        'mahallesi': r'([A-Za-zÇŞĞÜÖİçşğüöı\-]+(?: [A-Za-zÇŞĞÜÖİçşğüöı\-]+)*?) (mh\.|mah\.|mahallesi)\b',
        'bulvari': r'([A-Za-zÇŞĞÜÖİçşğüöı\-]+(?: [A-Za-zÇŞĞÜÖİçşğüöı\-]+)*?) (blv\.|blv|bulvar|boulevard)\b',
        'plazasi': r'([A-Za-zÇŞĞÜÖİçşğüöı\-]+(?: [A-Za-zÇŞĞÜÖİçşğüöı\-]+)*?) (plaza|plz\.|plz)\b',
        'rezidansi': r'([A-Za-zÇŞĞÜÖİçşğüöı\-]+(?: [A-Za-zÇŞĞÜÖİçşğüöı\-]+)*?) (rezidans|residence)\b',
        'ofisi': r'([A-Za-zÇŞĞÜÖİçşğüöı\-]+(?: [A-Za-zÇŞĞÜÖİçşğüöı\-]+)*?) (office|ofis)\b'
    }
    def perform_extraction(text, patterns):
        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                extracted = match.group(1)
                extracted = extracted.replace('i', 'İ').replace('ı', 'I').title()
                return f"{extracted} {key.title()}"
        return None

    # Fallback extraction method
    def fallback_extraction(text):
        # A more general extraction logic (e.g., extracting the first few words)
        words = text.split()
        if len(words) >= 2:
            return ' '.join(words[:2]).title()
        return ''

    # Handle non-existent or non-string addresses
    if address is None or pd.isna(address) or not isinstance(address, str):
        return ''

    address_lower = address.lower()

    # Initial extraction
    extracted = perform_extraction(address_lower, patterns)

    # Check for empty result and apply fallback
    if not extracted:
        extracted = fallback_extraction(address_lower)

    # Additional check for overly long or multiple address types
    words = extracted.split()
    if len(words) > 4 or sum(word in extracted for word in ['Sokagi', 'Caddesi', 'Mahallesi', 'Bulvari', 'Plazasi', 'Rezidansi', 'Ofisi']) > 1:
        extracted = perform_extraction(' '.join(words[-3:]), patterns)

    return extracted


sokak_count = cadde_count = mah_count = blv_count = plz_count = unknown_count = nan_count = resi_count = ofc_count = 0

# Apply the extract function to the 'loca' column
#data['extracted_loca'] = data['loca'].apply(extract)
# Apply the function to the DataFrame
#df['loca'] = df['address'].apply(extract)
vals_dict = {
    'sokak_count': sokak_count,
    'cadde_count': cadde_count,
    'mah_count': mah_count,
    'blv_count': blv_count,
    'unknown_count': unknown_count,
    'nan_count': nan_count,
    'plz_count': plz_count,
    'rezidans_count':resi_count,
    'office_count' : ofc_count
}

# Count the occurrences of each unique value in 'loca'
#loca_counts = df['loca'].value_counts()

# Print the number of 'unknown' occurrences
#unknown_count = loca_counts.get('unknown', 0)
#print(f"Number of values in loca: {loca_counts}")
#print(f"Number of 'unknown' in loca: {unknown_count}")
# Filter the DataFrame for rows where 'loca' is 'unknown'
#unknown_loca_df = df[df['loca'] == 'unknown']

# Get a random sample of these rows. Adjust the number in sample(n=5) to get more or fewer samples.
#unknown_loca_sample = unknown_loca_df.sample(n=5)

# Print the sample
#print("Sample rows where 'loca' is 'unknown':")
# Modify display options
#pd.set_option('display.max_colwidth', None)  # This will ensure full strings are displayed
#print(unknown_loca_sample[['address']])

#print(vals_dict)
#new_df = df[['address','loca']]
#df.to_csv('out_address_loca4.csv')


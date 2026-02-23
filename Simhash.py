import sys
import re
import requests
from bs4 import BeautifulSoup

# funtion for feching the text from the web page
def fetch_body(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        r = requests.get(url, headers=headers)
    except:
        print("url not opening :")
        sys.exit(1)

    soup = BeautifulSoup(r.text, "html.parser")

   
    for item in soup(["script", "style"]):
        item.extract()

    page_text = soup.get_text()
    return page_text


#funtion for counting the number of times each word appears in the text
def word_weight(text):

    text = text.lower()
    word_list = re.findall(r"[a-z0-9]+", text)

    word_frequency = {}

    for w in word_list:
        if w in word_frequency:
            word_frequency[w] += 1
        else:
            word_frequency[w] = 1

    return word_frequency


# funtion for calculating the polynomial hash of a word
def polynomial_hashing(word):
    o = 53
    k= 2**64
    hash_val = 0
    power = 1

    for char in word:
        hash_val = (hash_val + ord(char) * power) % k
        power = (power * o) % k

    return hash_val


# funtion for calculating the simhash of a document based on the frequency of words

def simhash_calculation(freq_dictionary):
    arr = [0] * 64
    for word in freq_dictionary:
        h = polynomial_hashing(word)
        count = freq_dictionary[word]
        for i in range(64):
            bit = (h >> i) & 1
            if bit:
                arr[i] += count
            else:
                arr[i] -= count

    simhash_result = 0
    for i in range(64):
        if arr[i] > 0:
            simhash_result = simhash_result | (1 << i)
    return simhash_result


# funtion for calculating the number of similar bits present in the two dcuments using the simhash
def similar_bits(hash_doc1, hash_doc2):
    similar_bits = hash_doc1 ^ hash_doc2
    different_bits_count = bin(similar_bits).count("1")
    return 64 - different_bits_count



if len(sys.argv) != 3:
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

body_text1 = fetch_body(url1)
body_text2 = fetch_body(url2)

freq1 = word_weight(body_text1)
freq2 = word_weight(body_text2)

simhash1 = simhash_calculation(freq1)
simhash2 = simhash_calculation(freq2)

common_bits = similar_bits(simhash1, simhash2)

print("\nSimhash_Of_web 1:", simhash1)
print("Simhash_Of_web 2:", simhash2)
print("\nCommon bits:", common_bits)


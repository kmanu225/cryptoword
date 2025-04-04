from utils import get_frequences, find_ngrams_distances, MIC, IC_fr
from cesar_frequence import decrypt_cesar, get_cesar_key, rot_left, rot_right


def vigenere_to_cesars(text, l):
    i = 0
    cesar_texts = []
    for i in range(l):
        cesar_text = ""
        for j in range(i, len(text), l):
            cesar_text += text[j]
        cesar_texts.append(cesar_text)
    return cesar_texts


def cesars_to_vigenere(cesar_texts):
    l = len(cesar_texts)
    text = ""
    for i in range(len(cesar_texts[0])):
        for j in range(l):
            if i < len(cesar_texts[j]):
                text += cesar_texts[j][i]
    return text


decrypt_vigenere_kasiski = lambda text, l:cesars_to_vigenere([decrypt_cesar(text) for text in vigenere_to_cesars(text, l)])


def decrypt_vigenere_mic(text, l):
    cypher_cesar_texts = vigenere_to_cesars(text, l)
    Y_0 = cypher_cesar_texts[0]

    delta_0 = get_cesar_key(get_frequences(Y_0))
    decrypted_cesar_texts = [rot_left(Y_0, delta_0)]
    for i in range(1, l):
        for delta in range(26):
            Y_i = cypher_cesar_texts[i]
            if MIC(Y_0, rot_right(Y_i, delta)) > IC_fr:
                decrypted_cesar_texts.append(rot_left(Y_i, delta_0 - delta))
    return cesars_to_vigenere(decrypted_cesar_texts)

def get_l_kasiski(text, l=3):
    # On recherche les plus grands divisueurs communs de ces distances
    distances = find_ngrams_distances(text, l)
    return distances[0], distances
        
        
if __name__ == "__main__":
    cypher_text = "zbpuevpuqsdlzgllksousvpasfpddggaqwptdgptzweemqzrdjtddefekeferdprrcyndgluaowcnbptzzzrbvpssfpashpncotemhaeqrferdlrlwwertlussfikgoeuswotfdgqsyasrlnrzppdhtticfrciwurhcezrpmhtpuwiyenamrdbzyzwelzucamrptzqseqcfgdrfrhrpatsepzgfnaffisbpvdblisrplzgnemswaqoxpdseehbeeksdptdttqsdddgxurwnidbdddplncsd"
    
    
    print(get_l_kasiski(cypher_text, 3))

    print(decrypt_vigenere_kasiski(cypher_text, 4))
    print(decrypt_vigenere_mic(cypher_text, 4))

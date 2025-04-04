from utils import IC, IC_fr
from vigenere_kasiski import decrypt_vigenere_kasiski, vigenere_to_cesars

# Indice de coïncidence mutuelle pour trouver la taille de la clef de chiffrement dans le cas dd'un chiffrement de Vigenère

def get_l_mic(cypher_text, max_l=10, ic_lg=IC_fr):
    for i in range(1, max_l + 1):
        mean_ic = 0
        cesar_texts = vigenere_to_cesars(cypher_text, i)
        for cesar_text in cesar_texts:
            mean_ic += IC(cesar_text)
        mean_ic /= len(cesar_texts)
        
        if mean_ic > ic_lg:
            print(
                f" {i} : {round(mean_ic, 3)} | delta_ic : {round(abs(mean_ic - IC_fr), 3)}"
            )

if __name__ == "__main__":
    cypher_text_1= "ufzbdemltfnlfgmoneefrttkophfeiuplbfxbtrmltfczfygipzjygblyyjivigpfpffveptmfmfavjyxbymfcisptpyhjeuvppmpemwejeiopjgpxbweqpgipwpygilrelmmciqcmtpioeinzmhyejeiuditpwqlhstpmpwslgpcrjpwqlvmpwfw"
           
    get_l_mic(cypher_text_1)
    print(decrypt_vigenere_kasiski(cypher_text_1, 3))

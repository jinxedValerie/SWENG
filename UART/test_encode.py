
print("welcher key soll benutzt werden?")
key_input=input()
key= int(key_input)

print("welche nachricht soll verschlüsselt werden? (keine Sonderzeichen)")
message_input=input()




def new_letter_fn(letter, case_offset, key):                       #97 lower, 65 upper 
    letter_num = ord(letter) - case_offset
    new_num = ((letter_num + key) % 26) +case_offset
    new_letter = chr(new_num)
    return new_letter




def encoder(message_in, key):
    message = message_in
    new_word = ""
    for letter in message:
        if ord(letter)==32:             #Leerzeichen
             new_letter = " "
        elif letter.islower():
             new_letter= new_letter_fn(letter, 97, key)
        else:
             new_letter= new_letter_fn(letter,65, key)
        new_word += new_letter
    return new_word


def decoder(message_in, key):
    message = message_in
    new_word = ""
    key_rev= -1 * key
    for letter in message:
        if ord(letter)==32:             #Leerzeichen
             new_letter = " "
        elif letter.islower():
             new_letter= new_letter_fn(letter, 97, key_rev)
        else:
             new_letter= new_letter_fn(letter,65, key_rev)
        new_word += new_letter
    return new_word


print(encoder(message_input,key))

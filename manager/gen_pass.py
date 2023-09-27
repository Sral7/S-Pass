import math
import random as r
def gen_pass(length,readable,uppercase,lowercase,numbers,symbols,seperate,words):
    password =[]*length

    if readable == 3:
        extra =[]
        if numbers == True:
            extra.append(r.choice('0123456789'))
        if symbols == True:
            extra.append(r.choice('!@#$%&*_+-=£€~'))
        if length - len(extra) > 5 and numbers or symbols:
            plus = 0
            if length > 10:
                plus = length//8
            extras = r.randint(math.ceil(length/16), math.ceil(length/8)+plus)  
            if numbers and words:
                for _ in range(extras):
                    extra.append(r.choice('0123456789!@#$%&*_+-=£€~'))
            elif numbers:
                for _ in range(extras):
                    extra.append(r.choice('0123456789'))
            elif symbols:
                for _ in range(extras):
                    extra.append(r.choice('!@#$%&*_+-=£€~'))
            print(extras)
        print(extra)


    
        with open('manager/static/files/text.txt') as f:
            words = f.read().splitlines()
        word_lists = [[] for _ in range(6)]

        for word in words:
            word_lists[len(word)-1].append(word)

        while len(password) < length-len(extra):
            if length-len(extra) - len(password) < 7:
                rem = length- len(extra) - len(password)
            else:
                rem = r.randint(1,6)

            word = r.choice(word_lists[rem-1])
            if uppercase == True:
                word = word.capitalize()
            for char in word:
                password.append(char)

        if r.random() < 0.7:
            return(''.join(password)+''.join(extra))
        else:
            return(''.join(extra)+''.join(password))


    if readable < 3:
        chars =['U','L','N','S']
        if uppercase == False:
            chars.remove('U')
        else:
            password.append('U')

        if lowercase == False:
            chars.remove('L')
        else:
            password.append('L')

        if numbers == False:
            chars.remove('N')
        else:
            password.append('N')
            
        if symbols == False:
            chars.remove('S')
        else:
            password.append('S')
        

        for _ in range(length-len(chars)):
            password.append(r.choice(chars))

        if seperate == False:        
            r.shuffle(password)
        else:
            if r.random() < 0.7:
                password.sort(key=lambda x: (x not in ['U', 'L'], x in ['N', 'S']))
            else:
                password.sort(key=lambda x: (x in ['U', 'L'], x not in ['N', 'S']))
        
        for index,char in enumerate(password):
            if readable == 2:
                weights = {'E': 14.7, 'T': 9.1, 'A': 10.2, 'O': 8.5, 'I': 8.0, 'N': 6.7, 'S': 6.3, 'R': 6.0, 'H': 4.1, 'D': 4.3, 'L': 4.0, 'U': 3.2, 'C': 2.8, 'M': 1.4, 'F': 2.2, 'Y': 1.0, 'W': 1.4, 'G': 1.5, 'P': 1.2, 'B': 1.5, 'V': 1.0, 'K': 0.5, 'X': 0.2, 'Q': 0.1, 'J': 0.2, 'Z': 0.1}
            if char == 'U':
                if readable == 2:
                    password[index] = r.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ',weights=list(weights.values()))[0]
                else:
                    password[index] = r.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            elif char == 'L':
                if readable == 2:
                    password[index] = r.choices('abcdefghijklmnopqrstuvwxyz',weights=list(weights.values()))[0]
                else:
                    password[index] = r.choice('abcdefghijklmnopqrstuvwxyz')
            elif char == 'N':
                password[index] = r.choice('0123456789')
            elif char == 'S':
                password[index] = r.choice('!@#$%&*_+-=£€~')
            
        print(''.join(password))




output =gen_pass(12,3,True,True,True,False,True,False)
print(output)
        



"""
List of most probable passwords and english names can be found, respectively, at:
- https://github.com/danielmiessler/SecLists/blob/master/Passwords/probable-v2-top12000.txt
- https://github.com/dominictarr/random-name/blob/master/middle-names.txt

Author: Raphael Vallat
Date: May 2018
Python 3

Modifications: Paul Mallard
Date: February 2024
Python 3

"""

import string
from time import time
from itertools import product
from numpy import loadtxt
import zipfile

def main():

    files_path = '/home/pmallard/Documents/Programmation/Python/fileEncryption/'
    pwd_file = 'probable-v2-top12000.txt'
    names_file = 'middle-names.txt'
    towns_file = 'communes.txt'
    zip_file = 'secret.zip' # zip -e -P [Password] secret.zip secret.txt
    
    # PASSWORD TESTED
    zip_file = 'azerty1234'
    # PASSWORD TESTED

    start = time()

    '''===================================================='''
    # 1) Comparing with most common passwords / first names
    '''===================================================='''   
    
    common_pass = loadtxt(files_path+pwd_file, dtype=str)
    cp = [c for c in common_pass] # common password list
    common_names = loadtxt(files_path+names_file, dtype=str)
    cn = [c for c in common_names] # common names list
    cnl = [c.lower() for c in common_names] # cn in lowercase
    common_towns = loadtxt(files_path+towns_file, dtype=str)
    ct = [c for c in common_towns] # common towns list (in France)

    for passwords in cp:
        if(openZip(zip_file,passwords)==True):
            #Password found (break)
            print('Strategy1.1 - Any common passwords')
            print("Time = %f seconds\n" % (time()-start))
            return
    
    for Names in cn:
        if(openZip(zip_file,Names)==True):
            print('Strategy1.2 - Any common names')
            print("Time = %f seconds\n" % (time()-start))
            return

    for names in cnl:
        if(openZip(zip_file,names)==True):
            print('Strategy1.3 - Any common names (lowercase)')
            print("Time = %f seconds\n" % (time()-start))
            return
    
    for towns in ct:
        if(openZip(zip_file,towns)==True):
            print('Strategy1.4 - Any common towns in France')
            print("Time = %f seconds\n" % (time()-start))
            return
        
    print("\nNo password found with Strategy 1")
    print("S1 = %f seconds\n" % (time()-start))
    
    '''======================================================='''
    # 2) Product of Digits and common Names / Towns / Password
    '''======================================================='''
    start2 = time()
    nb = 4
    for i in range(1,nb+1): # number of digits tested
        
        isize_digits = bruteForce(string.digits,i)
    
        for word in productGenerator(cn,isize_digits):
            if(openZip(zip_file,word)==True):
                #Password found (break)
                print('Strategy2.1 - Common name + Digits')
                print("Time = %f seconds\n" % (time()-start))
                return
        
        for word in productGenerator(ct[:4775],isize_digits): 
            # much quicker -> ct[:4775]
            if(openZip(zip_file,word)==True):
                print('Strategy2.3 - Town + Digits')
                print("Time = %f seconds\n" % (time()-start))
                return
            
        for word in productGenerator(cp,isize_digits): 
            if(openZip(zip_file,word)==True):
                print('Strategy2.4 - Common pwd + Digits')
                print("Time = %f seconds\n" % (time()-start))
                return

        # for word in productGenerator(cnl,isize_digits):
        #     if(openZip(zip_file,word)==True):
        #         print('Strategy2.2 - Common name(lw) + Digits')
        #         print("Time = %f seconds\n" % (time()-start))
        #         return
    
    print("\nNo password found with Strategy 2")
    print("S2 = %f seconds\n" % (time()-start2))

    '''==============================================='''
    # 3) Semi-bruteforce, knowing the first & last name
    '''==============================================='''

    start3 = time()
    fname = input("What is your first name? ")
    lname = input("What is your last name? ")
    start4 = time()

    ascii = [a for a in string.printable[:-5]]
    first_char = ascii
    first_char.append("")
    names = [fname,fname.title(),lname,lname.title()]

    for n in names:
        for x in first_char:
            for i in range(1,3): # 1-2P char tested
                any_char = bruteForce(ascii,i)
                for c in any_char:
                    if(openZip(zip_file,x+n+c)==True):
                        print('Strategy3 - ?+name+???')
                        print("Time S3 = %f seconds\n" % (time()-start))
                        return
        
    print("\nNo password found with Strategy 3")
    print("Time S3 = %f seconds" % (time()-start4))

    '''========================================='''
    # 4) Bruteforce, only MaJ tested on 1st char
    '''========================================='''

    start5 = time()

    nb1 = 4
    for i in range(1,nb1+1):
        values = bruteForce(string.printable[:-6],i,False) 
        
        for x in values:
            if(openZip(zip_file,x)==True):
                print('Strategy4 - Bruteforce(4), with only MaJ tested on 1st char')
                print("Time S4 = %f seconds\n" % (time()-start))
                return

    print("\nNo password found with Strategy 4")
    print("Time S4 = %f seconds" % (time()-start5))

    '''=========================='''
    # 5) Bruteforce, the hard way
    '''=========================='''

    start6 = time()

    nb2 = 4
    for k in range(1,nb2+1):
        values = bruteForce(string.printable[:-6],k) 
        
        for x in values:
            if(openZip(zip_file,x)==True):
                print('Strategy5 - Bruteforce(3), the hard way')
                print("Time S5 = %f seconds\n" % (time()-start6))
                return
    
    input_time = start4 - start3
    print("\nNo password found")
    print("Total time = %f seconds" % (time()-start-input_time))

''' Extract a password-protected ZIP file using a list of potential passwords '''
def openZip(zip_file, word):
    
    pwd=zip_file # only equality test for now

    if (word==pwd):
        print(f"\nPassword : '{word}' found")
        return True
    else:
        return False

    zip_path = '/home/pmallard/Documents/Programmation/Python/fileEncryption/'

    try:
        with zipfile.ZipFile(zip_path+zip_file) as zpf:
            zpf.extractall(path=zip_path, members = zpf.namelist(), pwd = bytes(x.encode('utf-8')))
            print(f"Successfully extracted {zip_file} with password: {x}")
            return True
    except:
        return False

""" Test multiple combinations with a given alphabet """
def bruteForce(alphabet,nb,Bool=True):

    list = [a for a in alphabet] # Creating a list with 1st char beeing in alphabet

    if Bool==False: # /!\ if Bool false : There are no uppercases (except i=0) 
        alphabet = [e for e in alphabet if e not in string.ascii_uppercase]

    for i in range(nb-1):
        new_list = [] # Generating bigger elements in list
        for str in list:
            for x in alphabet: # Adding every possible chars
                new_str = str + x
                new_list.append(new_str)
        list = new_list
    
    return list

""" Every combinations of 2 lists returned into 1 list """
def productGenerator(list1,list2):
    for x in list1:
        for y in list2:
            yield x+y # produce a value from the generator

#print("\n> nb = %d : Compteur = %d , t=%f seconds " % (nb,len(values[nb-1]),bruteforce_timing))
#print("files_timing = %f seconds" % (files_timing))
#print("bruteforce_timing(%d) = %f seconds" % (nb,bruteforce_timing))


if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    
    #main()

    t1 = time()
    for k in range(1,4):
        values = bruteForce(string.printable[:-6],k) 
        
        for x in values:
            print(values)
            
    print("Total time = %f seconds" % (time()-t1))

'''

TO DO : CREATE A EXCEL FOR THE TIME OF OPENZIP() ON DIFFERENT LIST SIZES

bruteforce(nb)

ascii = printable - punctuation
> nb = 1 : Compteur = 62 , t=0.000523 seconds
> nb = 2 : Compteur = 3844 , t=0.027078 seconds
> nb = 3 : Compteur =  238328 , t=3.019607 seconds
> nb = 4 : Compteur =  14776336 , t=119.056815 seconds

ascii = lowercases + digits
> nb = 1 : Compteur = 36 , t=0.000345 seconds
> nb = 2 : Compteur = 1296 , t=0.009091 seconds
> nb = 3 : Compteur = 46656 , t=0.523587 seconds
> nb = 4 : Compteur = 1679616 , t=14.080699 seconds

'''
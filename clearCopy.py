# old = ['A','B','C','D','E']
# new = ['A','B','C','D','E','F','G']

# old = ['A','B','C','D','E']
# new = ['C','D','E','F','G']

# old = ['A','B','B']
# new = ['B','B','B']

old = ['A','B','B']
new = ['B','B']

unread = []

for i in range(0,len(new)):
    comFlag=0
    for j in range(0,len(old)):
        #print (old[j],new[i])
        if (new[i]==old[j]):
            k=0
            while (i+k<len(new) and j+k<len(old) and new[i+k]==old[j+k]):
                k+=1
                if (j+k==len(old)):
                    break
            if (j+k==len(old)):
                unread = new[i+k:]
                comFlag=1
                break
    if (comFlag==1):
        break

if (comFlag==0):
    unread=new
print (unread)
print ('Done') 

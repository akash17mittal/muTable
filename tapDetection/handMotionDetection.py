vals = []
c=0
for l in open('C:/Ragini/Fall 22/Smart Cities/XY6.txt').readlines()[1:]:
    s = l.strip().split('.')

    #print("S", s)
    x = float(f"{s[1]}.{s[2]}")
    #print("X",x)
    y = float(f"{s[3]}.{s[4]}")
    #print("Y",y)
    
        #print("j")
  #  z = float(f"{s[4]}.{s[5]}")
 
    vals.append([x,y])
#print("vals", vals)
d = pd.DataFrame(vals)
plt.plot(d[0], 'blue', label="X axis")
plt.plot(d[1], 'red', label="Y axis")
plt.xlabel("Number of Samples")
plt.ylabel("Acceleration values across X and Y")
plt.legend()

zs1 = d[1].values
diffs1 = zs1[1:] - zs1[:-1]
plt.plot((diffs1[1:] - diffs1[:-1]), label="y axis")
zs2 = d[0].values
diffs2 = zs2[1:] - zs2[:-1]
if (diffs1>0.25 or diffs2>0.45):
    print("Start Image Processing on Camera")
#plt.plot(diffs, label="y-axis")
plt.legend()
plt.xlabel("Number of Samples")
plt.ylabel("$\Delta$y/$\Delta$t ")
plt.legend()

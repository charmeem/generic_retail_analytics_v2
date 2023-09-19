# # Adding suffixes and indentations to columns as per requirement

def indentation(hkpi,hlist):
    i=0
    while i<= len(hlist)-1:
        if i==0:
            # print(hkpi[hlist[i]])
            # print(hlist[i])
            hkpi[hlist[i]] =' ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==1:
            hkpi[hlist[i]] ='  ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==2:
            hkpi[hlist[i]] ='   ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==3:
            hkpi[hlist[i]] ='    ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==4:
            hkpi[hlist[i]] ='     ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==5:
            hkpi[hlist[i]] ='      ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==6:
            hkpi[hlist[i]] ='       ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==7:
            hkpi[hlist[i]] ='        ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==8:
            hkpi[hlist[i]] ='         ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==9:
            hkpi[hlist[i]] ='          ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==10:
            hkpi[hlist[i]] ='           ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'
        if i==11:
            hkpi[hlist[i]] ='            ' + hkpi[hlist[i]] + ' (' + hlist[i].replace('_','')[0:2] +')'

        i=i+1

    return hkpi

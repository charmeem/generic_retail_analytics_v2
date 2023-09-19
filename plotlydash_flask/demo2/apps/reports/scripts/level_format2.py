import importlib
import indent
importlib.reload(indent)

# Formating Functions- See geo_calc for detail
def sformat(hkpi,nat,hlevel,hlist):
    # hkpi.to_csv('hkpi.csv')

    # Appending (Sm) to make the indeces consistent with final table
    # Renaming all the indeces using lambda function
    hkpi = hkpi.rename(index=lambda ind: ' ' + ind + ' ('+ hlevel[0][0:2] + ')' )

    #appending '____' to (Sm)
    if len(hlist)==12:
        hkpi = hkpi.rename(index=lambda ind: ind+'___________')
    if len(hlist)==11:
        hkpi = hkpi.rename(index=lambda ind: ind+'__________')
    if len(hlist)==10:
        hkpi = hkpi.rename(index=lambda ind: ind+'_________')
    if len(hlist)==9:
        hkpi = hkpi.rename(index=lambda ind: ind+'________')
    if len(hlist)==8:
        hkpi = hkpi.rename(index=lambda ind: ind+'_______')
    if len(hlist)==7:
        hkpi = hkpi.rename(index=lambda ind: ind+'______')
    if len(hlist)==6:
        hkpi = hkpi.rename(index=lambda ind: ind+'_____')
    if len(hlist)==5:
        hkpi = hkpi.rename(index=lambda ind: ind+'____')
    if len(hlist)==4:
        hkpi = hkpi.rename(index=lambda ind: ind+'___')
    if len(hlist)==3:
        hkpi = hkpi.rename(index=lambda ind: ind+'__')
    if len(hlist)==2:
        hkpi = hkpi.rename(index=lambda ind: ind+'_')

    return hkpi

def mformat(hkpi,nat,hlevel,hlist):

    # Appending (Ma) to make the indeces consistent with final table
    # Renaming all the indeces using lambda function
    hkpi = hkpi.reset_index()
    # Appending (heirarchy) to make the indeces consistent with final table
    # Renaming all the indeces using lambda function
    hkpi = indent.indentation(hkpi,hlevel)

    # Setting columns back to indexes
    hkpi = hkpi.set_index([*hlevel])

    # Joining indexes
    hkpi.index = hkpi.index.map('_'.join)

    #appending '___' to (heirarchy)
    # print("hlist",len(hlist))
    # print("hlevel",len(hlevel))

    # Checking length of hlist as '_' varies
    if len(hlist)==11:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'__________')
        elif len(hlevel)==3:
            hkpi = hkpi.rename(index=lambda ind: ind+'_________')
        elif len(hlevel)==4:
            hkpi = hkpi.rename(index=lambda ind: ind+'________')
        elif len(hlevel)==5:
            hkpi = hkpi.rename(index=lambda ind: ind+'_______')
        elif len(hlevel)==6:
            hkpi = hkpi.rename(index=lambda ind: ind+'______')
        elif len(hlevel)==7:
            hkpi = hkpi.rename(index=lambda ind: ind+'_____')
        elif len(hlevel)==8:
            hkpi = hkpi.rename(index=lambda ind: ind+'____')
        elif len(hlevel)==9:
            hkpi = hkpi.rename(index=lambda ind: ind+'___')
        elif len(hlevel)==10:
            hkpi = hkpi.rename(index=lambda ind: ind+'__')
        elif len(hlevel)==11:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')

    if len(hlist)==11:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'_________')
        elif len(hlevel)==3:
            hkpi = hkpi.rename(index=lambda ind: ind+'________')
        elif len(hlevel)==4:
            hkpi = hkpi.rename(index=lambda ind: ind+'_______')
        elif len(hlevel)==5:
            hkpi = hkpi.rename(index=lambda ind: ind+'______')
        elif len(hlevel)==6:
            hkpi = hkpi.rename(index=lambda ind: ind+'_____')
        elif len(hlevel)==7:
            hkpi = hkpi.rename(index=lambda ind: ind+'____')
        elif len(hlevel)==8:
            hkpi = hkpi.rename(index=lambda ind: ind+'___')
        elif len(hlevel)==9:
            hkpi = hkpi.rename(index=lambda ind: ind+'__')
        elif len(hlevel)==10:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')


    if len(hlist)==10:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'________')
        elif len(hlevel)==3:
            hkpi = hkpi.rename(index=lambda ind: ind+'_______')
        elif len(hlevel)==4:
            hkpi = hkpi.rename(index=lambda ind: ind+'______')
        elif len(hlevel)==5:
            hkpi = hkpi.rename(index=lambda ind: ind+'_____')
        elif len(hlevel)==6:
            hkpi = hkpi.rename(index=lambda ind: ind+'____')
        elif len(hlevel)==7:
            hkpi = hkpi.rename(index=lambda ind: ind+'___')
        elif len(hlevel)==8:
            hkpi = hkpi.rename(index=lambda ind: ind+'__')
        elif len(hlevel)==9:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')

    if len(hlist)==9:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'_______')
        elif len(hlevel)==3:
            hkpi = hkpi.rename(index=lambda ind: ind+'______')
        elif len(hlevel)==4:
            hkpi = hkpi.rename(index=lambda ind: ind+'_____')
        elif len(hlevel)==5:
            hkpi = hkpi.rename(index=lambda ind: ind+'____')
        elif len(hlevel)==6:
            hkpi = hkpi.rename(index=lambda ind: ind+'___')
        elif len(hlevel)==7:
            hkpi = hkpi.rename(index=lambda ind: ind+'__')
        elif len(hlevel)==8:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')

    if len(hlist)==8:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'______')
        elif len(hlevel)==3:
            hkpi = hkpi.rename(index=lambda ind: ind+'_____')
        elif len(hlevel)==4:
            hkpi = hkpi.rename(index=lambda ind: ind+'____')
        elif len(hlevel)==5:
            hkpi = hkpi.rename(index=lambda ind: ind+'___')
        elif len(hlevel)==6:
            hkpi = hkpi.rename(index=lambda ind: ind+'__')
        elif len(hlevel)==7:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')

    if len(hlist)==7:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'_____')
        elif len(hlevel)==3:
            hkpi = hkpi.rename(index=lambda ind: ind+'____')
        elif len(hlevel)==4:
            hkpi = hkpi.rename(index=lambda ind: ind+'___')
        elif len(hlevel)==5:
            hkpi = hkpi.rename(index=lambda ind: ind+'__')
        elif len(hlevel)==6:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')

    if len(hlist)==6:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'____')
        elif len(hlevel)==3:
            hkpi = hkpi.rename(index=lambda ind: ind+'___')
        elif len(hlevel)==4:
            hkpi = hkpi.rename(index=lambda ind: ind+'__')
        elif len(hlevel)==5:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')

    if len(hlist)==5:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'___')
        elif len(hlevel)==3:
            hkpi = hkpi.rename(index=lambda ind: ind+'__')
        elif len(hlevel)==4:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')

    if len(hlist)==4:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'__')
        elif len(hlevel)==3:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')

    if len(hlist)==3:
        # This is second element as this hlevel starts from second element
        # First element already handled in sformat above
        if len(hlevel)==2:
            hkpi = hkpi.rename(index=lambda ind: ind+'_')

    return hkpi

def bformat(hkpi,nat):
    # Appending (Brand) to make the indeces consistent with final table
    # Renaming all the indeces using lambda function
    hkpi = hkpi.reset_index()
    hkpi['SM'] =' ' + hkpi['SM'] + ' (Sm)'
    hkpi['Vendor'] ='  ' + hkpi['Vendor'] + ' (Ma)'
    hkpi['Brand'] ='    ' + hkpi['Brand'] + ' (Ba)'

    # Setting columns back to indexes
    hkpi = hkpi.set_index(['SM','Vendor','Brand'])

    # Joining indexes
    hkpi.index = hkpi.index.map('_'.join)

    #appending '__' to (Ba)
    hkpi = hkpi.rename(index=lambda ind: ind+'__')

    return hkpi

def pformat(hkpi,nat):

    # Appending (PS) to make the indeces consistent with final table
    # Renaming all the indeces using lambda function
    hkpi = hkpi.reset_index()
    hkpi['SM'] =' ' + hkpi['SM'] + ' (Sm)'
    hkpi['Vendor'] ='  ' + hkpi['Vendor'] + ' (Ma)'
    hkpi['Brand'] ='    ' + hkpi['Brand'] + ' (Ba)'
    hkpi['PS'] ='   ' + hkpi['PS'] + ' (Ps)'

    # Setting columns back to indexes
    hkpi = hkpi.set_index(['SM','Vendor','Brand','PS'])

    # Joining indexes
    hkpi.index = hkpi.index.map('_'.join)

    #appending '_' to (Ps)
    hkpi = hkpi.rename(index=lambda ind: ind+'_')

    return hkpi

def skformat(hkpi,nat):

    # Transpose columns into rows and viceversa
    hkpi =hkpi.T
    #DRop Num_pf index
    if nat!=1:
        hkpi.index = hkpi.index.droplevel()
    # Reorder indeces and transpose month into column
    hkpi = hkpi.reorder_levels(['SM','Vendor','Brand','PS','SKU','Month']).unstack('Month')
    return hkpi

def format(hkpi,nat,hlevel,mhh,hlist):
    # print(nat,hlevel,mhh,hlist)
    # Format the Indexes to match with the  Base
    # This was needed to overcome duplicated Indeces while copying individual level tables to base

    # For single level of heirarchy in the template file
    if mhh ==0:
        if len(hlevel)==1:

            # hkpi.to_csv('hkpi.csv')
            hkpi = sformat(hkpi,nat,hlevel,hlist)
        else:
            hkpi = mformat(hkpi,nat,hlevel,hlist)
    else:
        hkpi = skformat(hkpi,nat,hlevel,hlist)

    return hkpi

#need "database" for inventory. Probably just a list

#need a database of characters

from comfy import generateImage

generate first turn

while true:
    from generated turn, parse if the location has changed from previous.
    if yes:
        parse and create background image prompt
        feed to comfy
        display new background

    display player image

    from generated turn, grab the characters using llm
    
    if character exists in prompt, then 
        -> check database if character(s) exist
        ---> iff new character do character gen

        display character image
    








    get users action/ turn/ dialogue whatever
    -> parse for validity. do they break the game rules? 

    parse inventory changes, and apply. 
    # i think here we will want to kind of plop the old inventory and the users prompt (plus full context... maybe?) and then have a model just check those changes, and apply. The kind of "story generation" model will remain as un-encumbered as possible, that should be the philosophy of this project.
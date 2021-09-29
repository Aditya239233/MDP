
def increment_id(tag):
    if tag == "error":
        filename = "errorarena"
    elif tag == "valid":
        filename = "validarena"
    elif tag == "gif":
        filename = "gif"


    file = open(f"./results/id/{filename}.txt","r")
    id_line = file.readline()
    file.close()

    curr_id = int(id_line.strip())
    file = open(f"./results/id/{filename}.txt","w")
    file.write(f"{curr_id+1}")
    file.close()
    
    return curr_id
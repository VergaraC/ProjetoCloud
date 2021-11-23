import os


def createKey(client,keyName:str):
    
    keyPair = client.create_keyPair(KeyName=keyName)

    privateKey = keyPair["KeyMaterial"]

    #chmod 400 permissions
    print("Writing Key")
    with os.fdopen(os.open(f"./{keyName}.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
        handle.write(privateKey)
    return keyPair

def deleteKey(client,keyName:str):
    keyPair = client.delete_keyPair(KeyName=keyName)
    print(f"removing {keyName} if exist")
    #chmod 400 permissions
    try:
        os.remove("./" + keyName + ".pem")
        
    except:
        pass
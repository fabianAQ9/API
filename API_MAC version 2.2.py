import netmiko 
import re
from netmiko import *


host1=(input("INGRESA LA IP:   "))
username=(input("INGRESA EL USUARIO:  "))
password=(input("INGRESA LA CONTRASEÑA:  "))

SW1= {
        "device_type":"cisco_ios",
        "host": host1,
        "username":username,
        "password":password,
        "port":"22",
        "secret":"cisco",
        }
        #se guardan las contraseñas para poder conecttarse con la suguinete linea de codigo
CONEX= netmiko.ConnectHandler(**SW1)
x = input("INGRESE LA MAC QUE QUIERES BUSCAR:  ")

   #1    00e8.0148.aec7    DYNAMIC     Fa0/13
   #1    28d2.446a.2b11    DYNAMIC     Fa0/24
   #1    68e4.3b30.610d    DYNAMIC     Fa0/23
#cambios = "".join(x) #le quitamos todos los putnos que teng a la mac para podeer lograr la comparacion con la tabla de mac address




while True:

    COMANDO = CONEX.send_command("sh mac address-table")
   

    #cam="".join(COMANDO)
    #COMANDO=re.sub("[.]","",COMANDO)
    
    el_comando = re.search(x, COMANDO)

    if el_comando is not None:
        
        tabla_de_mac = "show mac address-table address"+" "+x 
        conexion_tabla_mac = CONEX.send_command(tabla_de_mac)
       
        
    
        
        PORT = re.findall(r"\w\w\w?\d\/\d\/?\d?\d?", conexion_tabla_mac)
      
        PUERTO= (PORT[0]) #se encuentra el puerto
        print("")
        print("UBICACION DE LA MAC".center(60))
        print("-------------------------------------------------------")
        print("|", "MAC",(x).center(20),"|","PUERTO:", (PUERTO), "|" )
        print("--------------------------------------------------------")
        print("")
        cdp  = CONEX.send_command("sh cdp neigh")
        
        PUERTO2 = re.findall(r"(Gi|Fa)", cdp)#((Gi|Fa)|\d\/\d\/?\d?\d?)
        PUERTO3 = re.findall(r"(\d\/\d\/?\d?\d?)", cdp) #y tambien se encuentra en el puerto de vecino
        
        try:
       
            for w in range (0,20,2):
                PRT=(PUERTO2[w])
                PRT2=(PUERTO3[w])
                PRT3= (PRT)+(PRT2)


                if PRT3 == PUERTO:
                    
                    break        
        except IndexError:
            
            print("BUSQUEDA CONLUIDA")
            
            break
            
        PRT=(PUERTO2[w])
        PRT2=(PUERTO3[w])
        PRT3= (PRT)+(PRT2)
        
        posID=w//2
        posIP=w*2//2

        if PRT3 == PUERTO: #si los puerto son iguales, vuelve a entrar para posterirmente vover hacer lo anteriorr

            Ndet = CONEX.send_command("sh cdp neigh det")
            LaIP= re.findall(r"\d\d\d[.]\d\d?\d?[.]\d\d?\d?[.]\d\d?\d?", Ndet)
            ID= re.findall(r"Device.ID: ..?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?", Ndet)
            SWITCH = (ID[posID])
            IP =(LaIP[posIP])
            
            SW2= {
                    "device_type":"cisco_ios",
                    "host":IP,
                    "username":username,
                    "password":password,
                    "port":"22",
                    "secret":"cisco",
                 }
               
            CONEX= netmiko.ConnectHandler(**SW2)
            

            Hdet = CONEX.send_command("sh running-config | include hos")
            HOST= re.findall(r"[^hostname ]..?.?.?.?.?.?.?.?.?", Hdet)
            fd= (HOST[0])
            print("ACTUAL: ", fd)
            print("")
            print("UBICACION SWITCH.".center(60))
            print("------------------------------------------------------")
            print( "|","ESTAS EN EL SWICH: ","|", fd,SWITCH, ("|"))
            print("-------------------------------------------------------")
            print("")

    else:
        x=re.sub('[-]','', x)
        print(x)
        x=x.lower()
        x=list(x)
        x.insert(4, ".")
        x.insert(9, ".")
        x="".join(x)
      
    


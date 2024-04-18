import os
import random

def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    
    # demand per second from different directions
    pWE = 1. / 10
    pEW = 1. / 11
    pNS = 1. / 30
    
    # Create the 'data' directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    with open("data/cross.rou.xml", "w") as routes:
        routes.write("""<routes>
    <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
    <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>

    <route id="right" edges="51o 1i 2o 52i" />
    <route id="left" edges="52o 2i 1o 51i" />
    <route id="down" edges="54o 4i 3o 53i" />
""")
        
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < pWE:
                routes.write('    <vehicle id="right_%i" type="typeWE" route="right" depart="%i" />\n' % (vehNr, i))
                vehNr += 1
            if random.uniform(0, 1) < pEW:
                routes.write('    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />\n' % (vehNr, i))
                vehNr += 1
            if random.uniform(0, 1) < pNS:
                routes.write('    <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0"/>\n' % (vehNr, i))
                vehNr += 1
        
        routes.write("</routes>")

# Call the generate_routefile() function
generate_routefile()
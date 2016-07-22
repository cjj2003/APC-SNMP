from time import sleep
from pysnmp.entity.rfc3413.oneliner import cmdgen

commands=(
    # Identity
    ('upsBasicIdentModel',0),
    ('upsBasicOutputStatus',0),

    # Battery
    ('upsBasicBatteryStatus',0),           # str
    ('upsBasicBatteryTimeOnBattery',0),    # x10-2 (1/100) seconds
    ('upsHighPrecBatteryCapacity',0),      # % *10
    ('upsHighPrecBatteryTemperature',0),   # °C *10
    ('upsAdvBatteryRunTimeRemaining',0),   # x10-2 (1/100) seconds 
    ('upsHighPrecBatteryActualVoltage',0), # V *10

    # Input Voltage
    ('upsBasicInputPhase',0),             # 
    ('upsHighPrecInputLineVoltage',0),    # V *10
    ('upsHighPrecInputMaxLineVoltage',0), # V *10
    ('upsHighPrecInputMinLineVoltage',0), # V *10
    ('upsHighPrecInputFrequency',0),      # Hz *10
    ('upsAdvInputLineFailCause',0),       #

    # Output Voltage
    ('upsBasicOutputStatus',0),         #
    ('upsBasicOutputPhase',0),          # 
    ('upsHighPrecOutputVoltage',0),     # V *10
    ('upsHighPrecOutputFrequency',0),   # Hz *10
    ('upsHighPrecOutputLoad',0),        # % *10
    ('upsHighPrecOutputCurrent',0),     # A *10
    ('upsHighPrecOutputEfficiency',0),  # % *10
    ('upsHighPrecOutputEnergyUsage',0), # kWh *10
)

print("Create MIB Variables...")
mibVariables=[]
for cmd in commands:
    mibVariables.append(
        cmdgen.MibVariable('PowerNet-MIB',*cmd).addMibSource('/home/pi/APC-SNMP/CompiledMIBs')
    )

def heartbeat():
    cmdGen=cmdgen.CommandGenerator()
    indication,status,index,varBinds=cmdGen.getCmd(
        cmdgen.CommunityData('public', mpModel=0),
        cmdgen.UdpTransportTarget(('134.36.67.93',161)),
        *mibVariables
    )

    if indication: print(indication)
    else:
        if status:
            print("{} at {}".format(
                status.prettyPrint(),
                index and varBinds[int(errorIndex)-1] or '?'
            ))
        else:
            for name,val in varBinds:
                print("{} = {}".format(name.prettyPrint(), val.prettyPrint()))

print("Starting...")
while 1:
    try:
        print("Heartbeating...?")
        heartbeat()
        sleep(30)
    except KeyboardInterrupt: break

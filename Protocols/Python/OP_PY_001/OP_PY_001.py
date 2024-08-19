from opentrons import protocol_api

metadata = {
    'protocolName': 'Glycerol stocks from 96-well cultures', 
    'author': 'Felipe Xavier Buson', 
    'apiLevel': '2.12' 
    }

def run(protocol: protocol_api.ProtocolContext):
    culture_plate = protocol.load_labware('eppendorf_96_wellplate_2ml_deep', '1')

    destination_plates = [protocol.load_labware('biorad_96_wellplate_200ul_pcr', '2'),
                        protocol.load_labware('biorad_96_wellplate_200ul_pcr', '3'),
                        protocol.load_labware('biorad_96_wellplate_200ul_pcr', '5'),
                        protocol.load_labware('biorad_96_wellplate_200ul_pcr', '6')]

    glyc_res = protocol.load_labware('nest_1_reservoir_195ml', '4')

    tipracks_300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '7'),
                    protocol.load_labware('opentrons_96_tiprack_300ul', '8')]    

    p300_8 = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=tipracks_300)

    # CHANGE NUMBER OF COLUMNS USED HERE
    cols_no = 0

    protocol.comment('DISTRIBUTING GLYCEROL')
    p300_8.distribute(75, glyc_res['A1'],
                      sum([plate.rows()[0][0:cols_no] for plate in destination_plates], []),
                      change_tip='never', blow_out=True, blowout_location='source well')
    
    for col in range(cols_no):
        p300_8.pick_up_tip()
        
        protocol.comment('DISTRIBUTING CELLS IN COL ' + str(col+1))
        
        p300_8.aspirate(300, culture_plate.rows()[0][col].bottom(z=3.0))
        
        for plate in destination_plates:
            p300_8.dispense(75, plate.rows()[0][col])
            p300_8.touch_tip()
            
        protocol.comment('MIXING CELLS IN COL ' + str(col+1))
            
        for plate in destination_plates:
            p300_8.mix(3, 130, plate.rows()[0][col])
            
        p300_8.drop_tip()
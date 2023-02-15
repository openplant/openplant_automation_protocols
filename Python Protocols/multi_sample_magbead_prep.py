# -*- coding: utf-8 -*-
"""
Created on Sun May 29 10:55:38 2022

@author: Felipe
"""

from opentrons import protocol_api

metadata = {'apiLevel':'2.4'}

def run(protocol: protocol_api.ProtocolContext):

    plate_96 = protocol.load_labware('eppendorf_96_wellplate_2ml_deep', '2')
    plate_out = protocol.load_labware('eppendorf_96_wellplate_2ml_deep', '10')
    liquids_reservoir = protocol.load_labware_from_definition('enzymax_12_reservoir_20ml', '5')

    tiprack_1000 = protocol.load_labware('opentrons_96_tiprack_1000ul', '6')
    tiprack_300 = protocol.load_labware('opentrons_96_tiprack_300ul', '3')
        
    p1000 = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack_1000])
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_300])

    mag_module = protocol.load_module("magnetic module", '1')
    mag_plate = mag_module.load_labware('eppendorf_96_wellplate_2ml_deep', '1')
    
    samples = [plate_96['E1'], plate_96['E2'], plate_96['E3']]
    lysis_buff = liquids_reservoir['A1']
    neut_buff = liquids_reservoir['A2']
    wash_buff = liquids_reservoir['A3']
    ethanol = liquids_reservoir['A4']
    elut_buff = liquids_reservoir['A5']
    waste = liquids_reservoir['A12']

    protocol.comment('\n -- Adding lysis buffer -- \n')    
    for sample in samples:
        p300.transfer(120, lysis_buff, sample, mix_after = (5, 200))
    
    protocol.delay(minutes = 4)

    protocol.comment('\n -- Adding neutralization buffer -- \n')
    for sample in samples:
        p300.transfer(240, neut_buff, sample, mix_after = (5, 250))


    protocol.pause('Centrifuge the samples plate at 4000xg for  20 minutes')


    protocol.comment('\n -- Transferring to magnetic module -- \n')
    for sample in samples:
        p1000.pick_up_tip()
        p1000.aspirate(300, sample.bottom(z=3.0), rate=0.2)
        p1000.dispense(300, mag_plate[sample.well_name])
        p1000.drop_tip()
    
    protocol.comment('\n -- Adding ethanol -- \n')
    for sample in samples:
        p1000.transfer(300, ethanol, mag_plate[sample.well_name], mix_after = (5, 600))
    
    protocol.comment('\n -- Starting incubation routine for initial binding -- \n')
    for i in range(4):
    if i > 0:
        protocol.delay(minutes = 3)
    for sample in samples:
        p1000.pick_up_tip()
        p1000.flow_rate.dispense = 800
        p1000.mix(5, 400, mag_plate[sample.well_name])
        p1000.move_to(mag_plate[sample.well_name].top())
        p1000.flow_rate.dispense = 300
        p1000.blow_out()
        p1000.drop_tip()
    
    mag_module.engage()
    protocol.delay(minutes = 2)
    
    for sample in samples:
        p1000.pick_up_tip()
        p1000.aspirate(700, mag_plate[sample.well_name], rate=0.2)
        p1000.dispense(700, waste)
        p1000.drop_tip()
    mag_module.disengage()

    protocol.comment('\n -- Adding wash buffer -- \n')
    for sample in samples:
        p1000.pick_up_tip()
        p1000.aspirate(500, wash_buff)
        p1000.dispense(500, mag_plate[sample.well_name])
        p1000.flow_rate.dispense = 800
        p1000.mix(5, 400, mag_plate[sample.well_name])
        p1000.move_to(mag_plate[sample.well_name].top())
        p1000.flow_rate.dispense = 300
        p1000.blow_out()
        p1000.drop_tip()
    
    mag_module.engage()
    protocol.delay(minutes = 2)
    
    for sample in samples:
        p1000.pick_up_tip()
        p1000.aspirate(500, mag_plate[sample.well_name], rate=0.2)
        p1000.dispense(500, waste)
        p1000.drop_tip()
    mag_module.disengage()
    
    
    protocol.pause('Dry plate at 65°C for 20 minutes')
    
    protocol.comment('\n -- Adding elution buffer -- \n')
    for sample in samples:
        p300.transfer(100, elut_buff, mag_plate[sample.well_name], mix_after=(5, 80))
    
    
    protocol.comment('\n -- Starting incubation routine for elution -- \n')
    for i in range(4):
        if i > 0:
            protocol.delay(minutes = 1)
        for sample in samples:
            p300.pick_up_tip()
            p300.flow_rate.dispense = 800
            p300.mix(10, 80, mag_plate[sample.well_name])
            p300.move_to(mag_plate[sample.well_name].top())
            p300.flow_rate.dispense = 300
            p300.blow_out()
            p300.drop_tip()
    
    mag_module.engage(12)
    protocol.delay(minutes=2)
    
    # Pick up supernatant slowly
    for sample in samples:
        p300.pick_up_tip()
        p300.aspirate(100, mag_plate[sample.well_name], rate=0.2)
        p300.dispense(100, plate_out[sample.well_name])
        p300.drop_tip()

    mag_module.disengage()
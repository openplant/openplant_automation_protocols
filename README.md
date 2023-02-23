# OpenPlant Automation Protocols
The Open Bioeconomy Lab and the Earlham Institute are collaborating to validate and make available a library of protocols and automation scripts for the Opentrons OT2 platform. We hope this collection of protocols can inspire more researchers to adapt their workflows for automation, enabling a higher throughput and efficiency in general molecular biology work. 

## Getting started
Follow [Opentrons' official guidance](https://support.opentrons.com/s/ot2-get-started) on setting up the OT2 robot and its software. Here we provide protocols to be run on the  OT-2 robot with the current software version (v6.2.1 as of this writing) with GEN2 pipettes and modules. All custom labware needed is specified in 'Custom Labware' and will be indicared on specific protocol documents.
#### Protocol Designer protocols
Protocols made with [Opentrons' protocol designer](https://designer.opentrons.com/) can be visualized and edited within the designer. This is the most user-friendly way to interact with the protocols.
#### Python protocols
OT python protocols are made to give nuanced control of robot commands to the user, be easily customisable, and integrate the benefits of working with the python environment while still enabling the potocols to be run by researchers without programming experience. See the [Opentrons python API documentation](https://docs.opentrons.com/v2/) for reference on the code itself.
#### Jupyter notebooks
These protocols control the robot in a more granular, real-time (and incidentally hands-on) manner. While this allows for quick customization and prototyping, it also requires some understanding of python and Jupyter Notebooks to operate. Refer to [this article](https://support.opentrons.com/s/article/Running-the-robot-using-Jupyter-Notebook) for instructions on how to set up Jupyter Notebook-control on the robot.

## Licensing
All code is under an MIT license and all text is under CC0.

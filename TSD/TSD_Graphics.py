## The grapics class for the TSD program

import Parsers
import TSD

class TSD_Graphics:


	# The display graphics John made
    def UI(machine_name, percentage):



        return

    # Method the recalculates the total percentage
    ## are we looping through the entire RDY file and counting all the 1s and 2s?
    def calc_percent(machine_name, pass_type, current_machine_total_ones, current_machine_total_twos):

        if (pass_type == 1) :
                total_ones = current_machine_total_ones + 1

        else :
                total_twos = current_machine_total_twos + 1

        percentage = total_twos / total_ones

        if (total_ones > 5):
                UI(machine_name, total_ones)

        elif (total_twos > 5):
                UI(machine_name, total_twos)

        UI(machine_name, percentage)
        return total_ones, total_twos


main()

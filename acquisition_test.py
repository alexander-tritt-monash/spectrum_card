import spectrum_card as sc
import time as tm

digitiser = sc.Card(b"/dev/spcm0")
awg = sc.Card(b"/dev/spcm1")

digitiser.identification_led_enable()
tm.sleep(2)
digitiser.identification_led_disable()
awg.identification_led_enable()
tm.sleep(2)
awg.identification_led_disable()

awg.close()
digitiser.close()

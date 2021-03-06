__author__ = 'redragonx/daemoniclegend'

# future home for keyboard inputs
from plane_controller import plane_ctrl
import re
from io_package import audio


class User_keypad():
    pattern = re.compile("[0-9]{4}\#")
    __small_audio = audio()

    def keypad_input(self, codeIn):
        new_code = codeIn

        if len(new_code) == 5:
            if self.pattern.match(new_code):
                # Can include code later to "read back" the inputted code
                self.__small_audio.audio_alert('you_entered')
                for x in range(0, 3):
                    '''
                    if new_code.get(x) == 0:
                        self.__small_audio.audio_alert('0')
                        x += 1
                    elif new_code.get(x) == 1:
                        self.__small_audio.audio_alert('1')
                        x += 1 
                    elif new_code.get(x) == 2:
                        self.__small_audio.audio_alert('2') 
                        x += 1 
                    elif new_code.get(x) == 3:
                        self.__small_audio.audio_alert('3') 
                        x += 1 
                    elif new_code.get(x) == 4:
                        self.__small_audio.audio_alert('4') 
                        x += 1 
                    elif new_code.get(x) == 5:
                        self.__small_audio.audio_alert('5') 
                        x += 1 
                    elif new_code.get(x) == 6:
                        self.__small_audio.audio_alert('6') 
                        x += 1 
                    elif new_code.get(x) == 7:
                        self.__small_audio.audio_alert('7')
                        x += 1  
                    elif new_code.get(x) == 8:
                        self.__small_audio.audio_alert('8')
                        x += 1  
                    elif new_code.get(x) == 9:
                        self.__small_audio.audio_alert('9')
                        x += 1  
                    else:
                        break
                    '''

                outString = new_code[0:4]
                print(outString)
                plane_ctrl.update_transponder_code(outString)
                return 'Success'
            else:
                self.__small_audio.audio_alert('testfail')
                return 'Fail'
        else:
            self.__small_audio.audio_alert('bad_raw_data_error ')
            return 'Fail'

    def __init__(self):
        pass

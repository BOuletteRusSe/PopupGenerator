
from autoit import win_move as MoveWindow
from autoit.autoit import AutoItError
from os import startfile as StartFile
from time import sleep

popup_couter = 0

class Popup:
    
    def __init__(self, name, text):
        global popup_couter
        popup_couter += 1
        self.name = '{}{}'.format(name, popup_couter)
        self.text = text
        
class PopupsGenerator:
    
    def __init__(self):
        self.open_popups = dict()

    def Start(self, popups_count: int, ellips_time: float, name: str='Unkown ', text: str='Unkown', continue_update: bool=True):
        for i in range(popups_count):
            
            sleep(ellips_time)
            
            __popup__ = Popup(name, text)
            self.open_popups[__popup__.name] = [960, 540, True, True]
            _has_an_error_ = True
            self.CreatePopupFile(__popup__)
            
            while _has_an_error_:
                try:
                    StartFile(r'error.vbs')
                except FileNotFoundError:
                    self.CreatePopupFile(__popup__)
                else: _has_an_error_ = False
                    
            self.MovePopup()
            
        while continue_update:
            sleep(ellips_time)
            self.MovePopup()
                 
    def MovePopup(self):
        for pop, infos in self.open_popups.items():
            
            pos = [infos[0], infos[1]]
            _has_an_error_ = True
            
            while _has_an_error_:
                try:
                    MoveWindow(pop, pos[0], pos[1])
                except AutoItError:
                    pass
                else:
                    if pos[0] >= 1920-267: infos[2] = False
                    elif pos[0] <= 0: infos[2] = True
                    if pos[1] >= 1080-159: infos[3] = False
                    elif pos[1] <= 0: infos[3] = True
                    if infos[2]: self.open_popups[pop][0] = pos[0]+10
                    else: self.open_popups[pop][0] = pos[0]-10
                    if infos[3]: self.open_popups[pop][1] = pos[1]+10
                    else: self.open_popups[pop][1] = pos[1]-10
                    _has_an_error_ = False
                    
    @staticmethod
    def CreatePopupFile(__popup__):
        _has_an_errror_ = True
        while _has_an_errror_:
            try:
                with open('error.vbs', 'w+', encoding='utf-8') as err:
                    err.write('x = MsgBox("{}", 16+4096, "{}")'.format(__popup__.text, __popup__.name))
            except PermissionError:
                pass
            else:
                _has_an_errror_ = False

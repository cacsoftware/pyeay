
# -*- coding: utf-8 -*-

import wx
import wx.xrc
import  string

ALPHA_ONLY = 1
DIGIT_ONLY = 2
DIGIT_AND_PUNTO=3

class MyValidator(wx.PyValidator):
    def __init__(self, flag=None, pyVar=None):
        wx.Validator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return MyValidator(self.flag)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        if self.flag == ALPHA_ONLY:
            for x in val:
                if x not in string.ascii_letters:
                    return False

        elif self.flag == DIGIT_ONLY:
            for x in val:
                if x not in string.digits:
                    return False

        elif self.flag == DIGIT_AND_PUNTO:
            for x in val:
                if x not in '0123456789.':
                    return False

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if self.flag == ALPHA_ONLY and chr(key) in string.ascii_letters:
            event.Skip()
            return

        if self.flag == DIGIT_ONLY and chr(key) in string.digits:
            event.Skip()
            return

        if self.flag == DIGIT_AND_PUNTO and chr(key) in '0123456789.':
            event.Skip()
            return

        if not wx.Validator.IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

def validador_solo_digitos():
    return MyValidator(DIGIT_ONLY)

def validador_solo_letras():
    return MyValidator(ALPHA_ONLY)

def validador_solo_digitos_y_punto():
    return MyValidator(DIGIT_AND_PUNTO)
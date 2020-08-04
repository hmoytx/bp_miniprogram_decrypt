#!python
#!/usr/bin/env python
# -*- coding:utf-8 -*-


import base64
from java.util import Base64
from java.lang import String
from javax.crypto import Cipher
from javax.crypto.spec import IvParameterSpec, SecretKeySpec
from java.security import *
from burp import IBurpExtender, IProxyListener
from burp import IBurpExtender, ITab
from java.awt import Container,Dimension,Rectangle,Toolkit
from javax.swing import SwingConstants
from javax.swing import JPanel
from javax.swing import JButton
from javax.swing import JTextField
from javax.swing import JLabel
from javax.swing import JTextArea

class BurpExtender(IBurpExtender, ITab):

    def registerExtenderCallbacks(self, callbacks):

        self._cb = callbacks
        self._hp = callbacks.getHelpers()

        self._cb.setExtensionName('MiniProgram Decrypto')
        print 'successful!'

        self.mainPanel = JPanel()

        

        self.sessionKey = JLabel("sessionKey:")
        self.sessionKey.setHorizontalAlignment(SwingConstants.LEFT);
        
        self.iv = JLabel("iv:")
        self.tfsessionKey = JTextField(50)
        
        self.tfiv = JTextField(50)
        
        self.textAreaPlaintext = JTextArea(30, 40)
        self.textAreaPlaintext.setLineWrap(True)
        self.textAreaPlaintext2 = JTextArea(30, 40)
        self.textAreaPlaintext2.setLineWrap(True)
        self.DecryptoBtn = JButton('Decrypto >', actionPerformed=self.decrypto_onClick)
        self.CryptoBtn = JButton('< Crypto', actionPerformed=self.encrypto_onClick)
        
        self.mainPanel.add(self.sessionKey)
        self.mainPanel.add(self.tfsessionKey)
        self.mainPanel.add(self.iv)
        self.mainPanel.add(self.tfiv)
        
        self.mainPanel.add(self.textAreaPlaintext)
        self.mainPanel.add(self.CryptoBtn)
        self.mainPanel.add(self.DecryptoBtn)
        

        self.mainPanel.add(self.textAreaPlaintext2)

        self._cb.customizeUiComponent(self.mainPanel)
        self._cb.addSuiteTab(self)

    def decrypto_onClick(self, event):
        self.textAreaPlaintext2.setText("")
        session_key = self.tfsessionKey.getText()
        iv = self.tfiv.getText()
        payload = self.textAreaPlaintext.getText().rstrip()
        
        str = self.decrypto(payload, session_key, iv)
        
        self.textAreaPlaintext2.append(str)

    def encrypto_onClick(self, event):
        self.textAreaPlaintext.setText("")
        session_key = self.tfsessionKey.getText()
        iv = self.tfiv.getText()
        payload = self.textAreaPlaintext2.getText().rstrip()
        
        str = self.encrypto(payload, session_key, iv)
        
        self.textAreaPlaintext.append(String(str))


    def getTabCaption(self):
    	return 'MiniProgram Decrypto'

    def getUiComponent(self):
        return self.mainPanel


    def encrypto(self, payload, key, iv):
		aesKey = SecretKeySpec(base64.b64decode(key), "AES")
		aesIV = IvParameterSpec(base64.b64decode(iv))
		cipher = Cipher.getInstance("AES/CBC/PKCS7Padding")
		cipher.init(Cipher.ENCRYPT_MODE, aesKey, aesIV)
		encrypted = cipher.doFinal(payload)
		return Base64.getEncoder().encode(encrypted)


    def decrypto(self, payload, key, iv):
		decoded = base64.b64decode(payload)
		
		aesKey = SecretKeySpec(base64.b64decode(key), "AES")
		
		aesIV = IvParameterSpec(base64.b64decode(iv))
		
		cipher = Cipher.getInstance("AES/CBC/PKCS7Padding","BC")
		cipher.init(Cipher.DECRYPT_MODE, aesKey, aesIV)
		return String(cipher.doFinal(decoded)) 

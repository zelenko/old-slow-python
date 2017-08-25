#!/usr/bin/env python

"Forms example."

import sys, re, os
sys.path.append('../')
sys.path.append('../../')

import web.error; web.error.handle()
import web, web.form, web.form.field.basic, web.util

class ExampleForm(web.form.Form):
    
    def setup(self):
        self.addField(web.form.field.basic.Input('input', 'Default Text', 'Input Box:', size=14, maxlength=25))
        self.addField(web.form.field.basic.Password('password', 'Default Text', 'Password Field:',size=14, maxlength=25))
        self.addField(web.form.field.basic.Hidden('hiddenfield', 'Default Text','Hidden Field')) # XXX
        self.addField(web.form.field.basic.CheckBox('checkbox', 'DefaultValue', 'Checkbox:'))
        self.addField(web.form.field.basic.Button('button', 'Button Label', 'Button:'))
        self.addField(web.form.field.basic.TextArea('textarea', 'Text Area\n-----\nText', 'Text Area:'))
        self.addField(web.form.field.basic.RadioGroup('radiogroup', [('1','one'),('2','two'),('3','three')] , '3' , 'Radio Group:', align="table", cols=2))
        self.addField(web.form.field.basic.Menu('menu', [('1','one'),('2','two'),('3','three')], ['2','3'], 'Menu', size=3, required=False))
        self.addField(web.form.field.basic.Select('select', [('1','one'),('2','two'),('3','three')], '3', 'Select', required=True))
        self.addField(web.form.field.basic.CheckBoxGroup('checkboxgroup', [('1','one'),('2','two'),('3','three')], ['1','2'], 'Check Box Group:', required=True))
        self.addField(web.form.field.basic.Reset('reset', 'Reset', 'Reset Button:'))
        self.addField(web.form.field.basic.Submit('submit', 'Submit', 'Submit Button (normally not used):'))
        
        # The preffered way of adding submit buttons is as actions so Submit buttons are normally not used.
        self.addAction('Validate This Form')

    def valid(self):
        if web.form.Form.valid(self):
            validates = True
            if self.get('input').value == 'Default Text':
                self.get('input').setError("ERROR: You must change the text in the input box.")
                validates = False
            return validates
        else:
            return False

# Print the HTTP Header
print web.header('text/html')


# Create a form

exampleForm = ExampleForm('form', os.environ['SCRIPT_NAME'], 'get')

if len(web.cgi) > 0: # Form submitted
    # Populate form with the values from get.
    
    # Prepare form values:
    values = {}
    
    for k in web.cgi.keys():
        values[k] = [k,str(web.cgi[k])]
        if exampleForm.has_key(k):
            values[k].append(exampleForm[k].value)
            values[k].append(exampleForm[k].error())
    exampleForm.populate(web.cgi)

    for k in web.cgi.keys():
        if exampleForm.has_key(k):
            values[k].append(exampleForm[k].value)
            values[k].append(exampleForm[k].error())
            
    if exampleForm.valid():
        for k in web.cgi.keys():
            if exampleForm.has_key(k):
                values[k].append(exampleForm[k].value)
                values[k].append(exampleForm[k].error())
        valueText = ''
        for k in exampleForm.keys():
            if web.cgi.has_key(k):
                valueText += '<strong>%s</strong><br>'%values[k][0]
                valueText += '<table border="0">'
                valueText += '<tr><td>Create</td><td>%s</td></tr>'%web.encode(repr(values[k][2]))
                valueText += '<tr><td>Error</td><td>%s</td></tr>'%web.encode(repr(values[k][3]))
                valueText += '<tr><td>Populate</td><td>%s</td></tr>'%web.encode(repr(values[k][4]))
                valueText += '<tr><td>Error</td><td>%s</td></tr>'%web.encode(repr(values[k][5]))
                valueText += '<tr><td>Validate</td><td>%s</td></tr>'%web.encode(repr(values[k][6]))
                valueText += '<tr><td>Error</td><td>%s</td></tr>'%web.encode(repr(values[k][7]))
                valueText += '</table><br><br>'
        print "<html><head><title>Form Test - Validated</title></head><body>\n<h1>It Validated!</h1>%s\n<hr>\n<h2>Values</h2>%s</body></html>"%(exampleForm.frozen(), valueText)
    else:
        for k in web.cgi.keys():
            if exampleForm.has_key(k):
                values[k].append(exampleForm[k].value)
                values[k].append(exampleForm[k].error())
        valueText = ''
        for k in exampleForm.keys():
            if web.cgi.has_key(k):
                valueText += '<strong>%s</strong><br>'%values[k][0]
                valueText += '<table border="0">'
                valueText += '<tr><td>Create</td><td>%s</td></tr>'%web.encode(repr(values[k][2]))
                valueText += '<tr><td>Error</td><td>%s</td></tr>'%web.encode(repr(values[k][3]))
                valueText += '<tr><td>Populate</td><td>%s</td></tr>'%web.encode(repr(values[k][4]))
                valueText += '<tr><td>Error</td><td>%s</td></tr>'%web.encode(repr(values[k][5]))
                valueText += '<tr><td>Validate</td><td>%s</td></tr>'%web.encode(repr(values[k][6]))
                valueText += '<tr><td>Error</td><td>%s</td></tr>'%web.encode(repr(values[k][7]))
                valueText += '</table><br><br>'
        print "<html><head><title>Form Test - Errors</title></head><body>\n<h1>Please Check Entries</h1>%s\n<hr>\n<h2>Values</h2>%s</body></html>"%(exampleForm.html(), valueText)
else:
    print "<html><head><title>Form Test</title></head><body>\n<h1>Welcome Please Fill In The Form</h1>%s\n<hr></body></html>"%(exampleForm.html())
import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd

# GUI code

sg.theme('LightGreen1')

# Excel read code

EXCEL_FILE = 'Articulated_V3_FK.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay-out code


layout = [
    [sg.Push(), sg.Text(' Articulated Manipulator Design Calculator', font =("Cambria",15)),sg.Push()],
    [sg.Text('Forward Kinematics Calculator',font=("Cambria",12))],
    [sg.Text('Fill out the following fields:',font=("Cambria",13)),
    sg.Push(), sg.Push(), sg.Button('Click this before Solving Forward Kinematics',font=("Cambria",15),size=(38,0),button_color=('white','gray')), sg.Push(),], 

    [sg.Text('a1 = ', font = ("Cambria",10)),sg.InputText('70', key='a1', size=(20,10)),
    sg.Text('T1 = ', font = ('Cambria',10)),sg.InputText('0', key='T1',size=(20,10)),
    sg.Push(),sg.Button('Jacobian Matrix (J)', font = ("Cambria",12), size=(15,0), button_color=('white','darkred')), 
    sg.Button('Det(J)', font = ("Cambria",12), size=(15,0), button_color=('white','darkred')),
    sg.Button('Inverse of J', font = ("Cambria",12), size=(15,0), button_color=('white','darkred')),
    sg.Button('Transpose of J', font = ("Cambria",12), size=(15,0), button_color=('white','darkred')), sg.Push()],

    [sg.Text('a2 = ', font = ("Cambria",10)),sg.InputText('75',key='a2', size=(20,10)),
    sg.Text('T2 = ', font = ("Cambria",10)),
    sg.InputText('0',key='T2', size=(20,10)),
    sg.Push(),sg.Button('Solve Forward Kinematics', font = ("Cambria",15), button_color=('white','gray')), sg.Push(),],

    [sg.Text('a3 = ', font = ("Cambria",10)),
    sg.InputText('30',key='a3', size=(20,10)),
    sg.Text('T3 = ', font = ("Cambria",10)),
    sg.InputText('0',key='T3', size=(20,10)),
    sg.Push(), sg.Button('Inverse Kinematics', font = ("Cambria",15), size=(35,0), button_color=('white','yellowgreen')),sg.Push(),
    sg.Push(), sg.Button('Path and Trajectory Planning', font = ("Cambria",15), size=(40,0), button_color=('white','yellowgreen')),sg.Push()],

    [sg.Frame('Position Vector: ',[[
        sg.Text('X = ', font = ("Cambria",10)),sg.InputText(key = 'X', size = (10,1)),
        sg.Text('Y = ', font = ("Cambria",10)),sg.InputText(key = 'Y', size = (10,1)),
        sg.Text('Z = ', font = ("Cambria",10)),sg.InputText(key = 'X', size = (10,1))]])],

    [sg.Push(),sg.Frame('H0_3 Transformation Matrix & Position Vector = ',[[sg.Output(size=(60,12))]]),
    sg.Push(),sg.Image('CART2.gif'), sg.Push()],
    [sg.Submit(font = ("Cambria",10)),sg.Exit(font = ("Cambria",10))],
    ]

# Window code
window = sg.Window('Articulated Manipulator Design Calculator - Forward Kinematics',layout,resizable = True)

#Variable codes for solving disabling button

disable_J = window['Jacobian Matrix (J)']
disable_DetJ = window['Det(J)']
disable_IJ=  window['Inverse of J']
disable_TJ =  window['Transpose of J']
disable_IK =  window['Inverse Kinematics']
disable_PT = window['Path and Trajectory Planning']

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Click this before Solving Forward Kinematics':
        disable_J.update(disabled = True)
        disable_DetJ.update(disabled = True)
        disable_IJ.update(disabled = True)
        disable_TJ.update(disabled = True)
        disable_IK.update(disabled = True)
        disable_PT.update(disabled = True)

    if event == 'Solve Forward Kinematics':
        # Forward Kinematic Codes
        a1 = float(values['a1'])
        a2 = float(values['a2'])
        a3 = float(values['a3'])

        T1 = float(values['T1'])
        T2 = float(values['T2'])
        T3 = float(values['T3'])

        T1 = (T1/180.0)*np.pi # Theta 1 in radians
        T2 = (T2/180.0)*np.pi # Theta 2 in radians
        T3 = (T3/180.0)*np.pi # Theta 3 in radians

        DHPT = [[T1,(90.0/180.0)*np.pi,0,a1],
            [T2,(0.0/180.0)*np.pi,a2,0],
            [T3,(0.0/180.0)*np.pi,a3,0]]
        
        i = 0
        H0_1 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
        [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
        [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
        [0,0,0,1]]

        i = 1
        H1_2 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
        [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
        [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
        [0,0,0,1]]

        i = 2
        H2_3 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
        [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
        [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
        [0,0,0,1]]   

        H0_1 = np.matrix(H0_1)

        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)
        print(np.matrix(H0_1)) 
        print(np.matrix(H0_2)) 
        print(np.matrix(H0_3)) 

        X0_3 = H0_3[0,3]
        print("X = ", X0_3)

        Y0_3 = H0_3[1,3]
        print("Y = ", Y0_3)

        Z0_3 = H0_3[2,3]
        print("Z = ", Z0_3)

        disable_J.update(disabled = False)
        disable_IK.update(disabled = False)
        disable_PT.update(disabled = False)

    if event == 'Submit':
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!')
    
    if event == 'Jacobian Matrix (J)':
        
        Z_1 = [[0],[0],[1]] # The 0 0 1 vector
        IM = [[1,0,0], [0,1,0],[0,0,1]]
        d0_3 = H0_3[0:3,3:]

        # row 1 to 3 columm 1
        
        J1a = np.dot(IM,Z_1)

        
        #print('J1 = ')
        #print(np.matrix(J1))
        
        J1 = [
            [(J1a[1,0]*d0_3[2,0])-(J1a[2,0]*d0_3[1,0])],
            [(J1a[2,0]*d0_3[0,0])-(J1a[0,0]*d0_3[2,0])],
            [(J1a[0,0]*d0_3[1,0])-(J1a[1,0]*d0_3[0,0])]]

       # Row 1 - 3 column 2
        R0_1a = np.dot(H0_1,1)
        R0_1b = R0_1a[0:3, 0:3]
        d0_1 = R0_1a[0:3,3:]
        J2a = (np.dot(R0_1b,Z_1))
        J2b = (np.subtract(d0_3,d0_1))

        # Cross product of Row 1 - 3 column 2|

        J2 = [
            [(J2a[1,0]*J2b[2,0])-(J2a[2,0]*J2b[1,0])],
            [(J2a[2,0]*J2b[0,0])-(J2a[0,0]*J2b[2,0])],
            [(J2a[0,0]*J2b[1,0])-(J2a[1,0]*J2b[0,0])]
            ]

        # Row 1 - 3 column 3
       
        R0_2 = H0_2[0:3, 0:3]
        d0_2 = H0_2[0:3,3:]
        J3a = (np.dot(R0_2,Z_1))
        J3b = (np.subtract(d0_3,d0_2))

        # Cross product of Row 1 - 3 column 3

        J3 = [
            [(J3a[1,0]*J3b[2,0])-(J3a[2,0]*J3b[1,0])],
            [(J3a[2,0]*J3b[0,0])-(J3a[0,0]*J3b[2,0])],
            [(J3a[0,0]*J3b[1,0])-(J3a[1,0]*J3b[0,0])]
            ]

        JM1 = np.concatenate((J1,J2,J3),1)
        #print(JM1)
        JM2 = np.concatenate((J1a,J2a,J3a),1)
        #print(JM2)

        J = np.concatenate((JM1, JM2),0)
        #print("J = ")
        #print(J)

        print(np.matrix(d0_3)) 
        sg.popup('J = ', J)

        disable_J.update(disabled =True)
        disable_DetJ.update(disabled =False)
        disable_IJ.update(disabled =False)
        disable_TJ.update(disabled =False)

        try: 
            H0_3 = np.matrix(H0_1)
        except:
            H0_3 = -1

            sg.popup('warning!')
            sg.popup('Restart the GUI then go first to "Click this before Solving Forward Kinematics"!')
            break

    if event == 'Det(J)':
        #singularity =Det(J)
        #np.linalg.det(M)
        #Let JM1 become the 3X3 position matrix for obtaining the Determinant

        try: 
            JM1 = np.concatenate((J1,J2,J3),1)
            
        except:
            JM1 = -1

            sg.popup('warning!')
            sg.popup('Restart the GUI then go first to "Click this before Solving Forward Kinematics"!')
            break

        DJ = np.linalg.det(JM1)
        #print("DJ = ", DJ)

        sg.popup('DJ = ',DJ)

        if DJ == -0.0E-20 <= 0 <= 0.0E-20:
            disable_IJ.update(disabled =True)
            sg.popup('Warning: Jacobian Matrix is Non-invertable!')

    if event == 'Inverse of J':
        #Inv(J)

        try: 
            JM1 = np.concatenate((J1,J2,J3),1)
            
        except:
            JM1 = -1

            sg.popup('warning!')
            sg.popup('Restart the GUI then go first to "Click this before Solving Forward Kinematics"!')
            break
        
        IJ =np.linalg.inv(JM1)
        #print("IV = ")
        #print(IV)
        sg.popup('IJ = ', IJ)

    if event == 'Transpose of J':
        TJ = np.transpose(JM1)
        #print("TJ = ")
        #print(TJ)

        try: 
            JM1 = np.concatenate((J1,J2,J3),1)
            
        except:
            JM1 = -1

            sg.popup('warning!')
            sg.popup('Restart the GUI then go first to "Click this before Solving Forward Kinematics"!')
            break
        
        sg.popup('TJ = ', TJ)

window.close() 

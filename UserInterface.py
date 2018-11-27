import wx
import os
import serial
import glob
'''ser=serial.Serial('/dev/ttyACM0',38400)
s=ser.readline().split()
k=map(float,s)
print k
'''
import time
flag=0
patient_name=''
#ser=serial.Serial('/dev/ttyACM0',38400)
patient_file=''
reference_file='doctor.txt'
class Welcomepage(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'MESEBONPHY',size=(800,600))
        panel=wx.Panel(self)
        
        custom=wx.StaticText(panel, -1, " MEMS SENSOR BASED ONLINE PHYSIOTHERAPY ", (200,20),(360,-1), wx.ALIGN_CENTER)
        
        custom.SetForegroundColour('blue')
        
        #custo=wx.StaticText(panel, -1, " Thank You ", (380,550),(260,-1), wx.ALIGN_CENTER)
        #custo.SetForegroundColour('red')
	img1 = wx.Image('physio1.jpg', wx.BITMAP_TYPE_ANY)
	sb1 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img1),pos=(200,100))
        button=wx.Button(panel,label='Therapist',pos=(120,400),size=(200,40))
        butto=wx.Button(panel,label='Patient',pos=(500,400),size=(200,40))
        #butt=wx.Button(panel,label='Exit',pos=(740,520),size=(40,40))
        
        self.Bind(wx.EVT_BUTTON,self.Onbutton, button)
        self.Bind(wx.EVT_BUTTON,self.Onbutto,butto)
        #self.Bind(wx.EVT_BUTTON,self.closebutton, butt)
        self.Bind(wx.EVT_CLOSE,self.closewindow)
        

    def Onbutton(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Therapistpage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def Onbutto(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Patientpage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    #def closebutton(self,event):
        #self.Close(True)

    def closewindow(self,event):
        self.Destroy()

class Therapistpage(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'MESEBONPHY',size=(800,600))
        panel=wx.Panel(self)

        custom=wx.StaticText(panel, -1, " MEMS SENSOR BASED ONLINE PHYSIOTHERAPY ", (200,20),(360,-1), wx.ALIGN_CENTER)
        custo=wx.StaticText(panel, -1, " Welcome Doctor ", (200,40),(360,-1), wx.ALIGN_CENTER)
        custom.SetForegroundColour('blue')
	info=wx.StaticText(panel, -1, " Please select the patients file and doctor file before checking patients performance ", (100,550),(360,-1), wx.ALIGN_CENTER)
        info.SetForegroundColour('red')        
	custo.SetForegroundColour('blue')
	img1 = wx.Image('therapy.png', wx.BITMAP_TYPE_ANY)
	sb1 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img1),pos=(200,100))
        button=wx.Button(panel,label='Record Exercise',pos=(70,500),size=(200,40))
        butto=wx.Button(panel,label='Exercise Files',pos=(500,500),size=(200,40))
        butt=wx.Button(panel,label='Patient Performance',pos=(285,500),size=(200,40))
        but=wx.Button(panel,label='Back',pos=(20,20),size=(80,40))
        
        self.Bind(wx.EVT_BUTTON,self.Onbutton, button)
        self.Bind(wx.EVT_BUTTON,self.Onbutto,butto)
        self.Bind(wx.EVT_BUTTON,self.Onbutt, butt)
        self.Bind(wx.EVT_BUTTON,self.Onbut,but)
        self.Bind(wx.EVT_CLOSE,self.closewindow)
        

    def Onbutton(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=TherapistRecordingpage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def Onbutto(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Exercisepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def Onbutt(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Performancepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()

    def Onbut(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Welcomepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def closewindow(self,event):
        self.Destroy()
'''-----------------------------------------------------------------######################################------------------------------'''
class Performancepage(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'MESEBONPHY',size=(800,600))
        panel=wx.Panel(self)
	global patient_name
	print patient_name
        custom=wx.StaticText(panel, -1, " ONLINE PHYSIOTHERAPY EVALUATION", (200,20),(360,-1), wx.ALIGN_CENTER)
        name=wx.StaticText(panel, -1, "Name : "+ patient_name, (50,100),(360,-1), wx.ALIGN_CENTER)
        custom.SetForegroundColour('blue')
	info=wx.StaticText(panel, -1, "  ", (100,550),(360,-1), wx.ALIGN_CENTER)
        info.SetForegroundColour('red')        
	
	img1 = wx.Image('hands.jpg', wx.BITMAP_TYPE_ANY)
	sb1 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img1),pos=(500,70))
        but=wx.Button(panel,label='Back',pos=(20,20),size=(80,40))
	anim=wx.Button(panel,label='View animation',pos=(50,450),size=(80,40))
	self.Bind(wx.EVT_BUTTON,self.Onanim,anim)        
	self.Bind(wx.EVT_BUTTON,self.Onbut,but)
        self.Bind(wx.EVT_CLOSE,self.closewindow)
	f=open(patient_name+'.txt','r')
	g=open('doctor.txt','r')
	fr=f.readline()
	gr=g.readline()
	shroll=0
	shpitch=0
	elroll=0
	elpitch=0
	sh_mean_deviation=0
	el_mean_deviation=0
	el_roll_variance=0
	sh_pitch_variance=0
	sh_roll_variance=0
	el_pitch_variance=0
	count=0
	while fr !='' or gr !='':
	
	
		fr=f.readline()
		gr=g.readline()
		frs=fr.split()
		grs=gr.split()
		if len(grs) ==6 and len(frs) ==6:
		
			shroll=	float(frs[1])-float(grs[1])
			shpitch=float(frs[2])-float(grs[2])
			elroll=float(frs[4])-float(grs[4])
			elpitch=float(frs[5])-float(grs[5])
			if abs(elroll)>30 or abs(shroll>30) or abs(shpitch)>30 or abs(elpitch)>30:
				continue
			else:
				sh_roll_variance+=abs(shroll)
				el_roll_variance+=abs(elroll)
				sh_pitch_variance+=abs(shpitch)
				el_pitch_variance+=abs(elpitch)
				count+=1	
				print shroll,shpitch,elroll,elpitch,count
						
	#print int(sh_roll_variance/count),int(sh_pitch_variance/count),int(el_roll_variance/count),int(el_pitch_variance/count)
	shpd=wx.StaticText(panel, -1, "shoulder pitch deviation : "+str(sh_pitch_variance/1000), (50,150),(360,-1), wx.ALIGN_CENTER)
        shrd=wx.StaticText(panel, -1, "shoulder roll deviation : "+str(sh_roll_variance/1000), (50,200),(360,-1), wx.ALIGN_CENTER)
        elpd=wx.StaticText(panel, -1, "elbow pitch deviation : "+str(el_pitch_variance/1000), (50,250),(360,-1), wx.ALIGN_CENTER)
        elrd=wx.StaticText(panel, -1, "elbow roll deivation : "+str(el_roll_variance/1000), (50,300),(360,-1), wx.ALIGN_CENTER)
	pcls=wx.StaticText(panel, -1, "no.of iterations : "+ "4", (50,350),(360,-1), wx.ALIGN_CENTER)
        timetaken=wx.StaticText(panel, -1, "Time taken : "+ "10", (50,400),(360,-1), wx.ALIGN_CENTER)
        

	print sh_roll_variance/count,sh_pitch_variance/count,el_roll_variance/count,el_pitch_variance/count        

    def Onanim(self,event):
	global patient_name
	print patient_name
        self.Destroy()
	os.system('python newm.py '+patient_name)	

    def Onbut(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Therapistpage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def closewindow(self,event):
        self.Destroy()

class Exercisepage(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'MESEBONPHY',size=(800,600))
        self.panel=wx.Panel(self)
	i=0
        self.custom=wx.StaticText(self.panel, -1, " MEMS SENSOR BASED ONLINE PHYSIOTHERAPY ", (200,20),(360,-1), wx.ALIGN_CENTER)
        self.custo=wx.StaticText(self.panel, -1, " Welcome Doctor, Here are the patient files  ", (200,40),(360,-1), wx.ALIGN_CENTER)
	self.dir=wx.StaticText(self.panel, -1, " Directory: /home/pavithran/pywk/... ", (200,80),(360,-1), wx.ALIGN_CENTER)
                
	self.custom.SetForegroundColour('blue')
        self.custo.SetForegroundColour('red')
	self.a=glob.glob("/home/pavithran/pywk/*.txt") 	
	self.lc = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT,size=(293,len(self.a)*30),pos=(200,100))
        self.lc.InsertColumn(0, 'Patient Name')
 	self.lc.InsertColumn(1, 'Text file')
        self.lc.SetColumnWidth(0, 140)
        self.lc.SetColumnWidth(1, 153)
	
        self.button=wx.Button(self.panel,label='Main Menu',pos=(100,450),size=(120,40))
        self.butto=wx.Button(self.panel,label='Delete File',pos=(300,450),size=(120,40))
        self.butt=wx.Button(self.panel,label='Select for report',pos=(500,450),size=(120,40))
        self.but=wx.Button(self.panel,label='Back',pos=(20,20),size=(80,40))
	for x in self.a:
		#print x
		x=x.split("/")
		
   		self.lc.InsertStringItem(i,x[4])
   	 	self.lc.SetStringItem(i, 1, x[4])
		i=i+1
	#self.lc.InsertStringItem(2, self.tc1.GetValue())
        #self.lc.SetStringItem(2, 1, self.tc2.GetValue())
        self.Bind(wx.EVT_BUTTON,self.Onbutton, self.button)
        self.Bind(wx.EVT_BUTTON,self.Onbutto,self.butto)
        self.Bind(wx.EVT_BUTTON,self.Onbutt, self.butt)
        self.Bind(wx.EVT_BUTTON,self.Onbut,self.but)
        self.Bind(wx.EVT_CLOSE,self.closewindow)
        

    def Onbutton(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Welcomepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def Onbutto(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Exercisepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def Onbutt(self,event):

	global patient_name	
	index = self.lc.GetFocusedItem()
	print index
	
	k= self.a[index].split('/')
	n=k[4].split('.')
	patient_name=n[0]	
	self.indexlabel=wx.StaticText(self.panel, -1, k[4] + " was selected ", (200,480),(360,-1), wx.ALIGN_CENTER)
	

    def Onbut(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Therapistpage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def closewindow(self,event):
        self.Destroy()
       
'''-----------------------------------------------------------------------------#############################################-----------'''
'''-----------------------------------------------------------------------------#############################################-----------'''  

class Patientpage(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'MESEBONPHY',size=(800,600))
        panel=wx.Panel(self)
	global patient_name
        box=wx.TextEntryDialog(None, "Username ", "MESEBONPHY", "Enter the your Name")
        if box.ShowModal()==wx.ID_OK:
            answer=box.GetValue()
            patient_name=answer
        custom=wx.StaticText(panel, -1, " MEMS SENSOR BASED ONLINE PHYSIOTHERAPY ", (200,20),(360,-1), wx.ALIGN_CENTER)
  	warn=wx.StaticText(panel, -1, " Please connect the device before continuing... ", (50,550),(360,-1), wx.ALIGN_CENTER)
        custo=wx.StaticText(panel, -1, " Welcome " + answer, (200,40),(360,-1), wx.ALIGN_CENTER)
        custom.SetForegroundColour('blue')
        custo.SetForegroundColour('blue')
	warn.SetForegroundColour('red')
	img1 = wx.Image('physio.jpg', wx.BITMAP_TYPE_ANY)
	sb1 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img1),pos=(50,75))
        button=wx.Button(panel,label='Main Menu',pos=(500,450),size=(120,40))
        exe1=wx.Button(panel,label='Arms',pos=(550,100),size=(120,40))
	exe2=wx.Button(panel,label='Legs',pos=(550,150),size=(120,40))
        exe3=wx.Button(panel,label='Wrist',pos=(550,200),size=(120,40))
        exe4=wx.Button(panel,label='Ankle',pos=(550,250),size=(120,40))
        exe5=wx.Button(panel,label='Hip',pos=(550,300),size=(120,40))
        exe6=wx.Button(panel,label='neck',pos=(550,350),size=(120,40))
                
	but=wx.Button(panel,label='Back',pos=(20,450),size=(80,40))
        
        self.Bind(wx.EVT_BUTTON,self.Onbutton, button)
        self.Bind(wx.EVT_BUTTON,self.Onbutto,exe1)
        self.Bind(wx.EVT_BUTTON,self.Onbutto,exe2)
	self.Bind(wx.EVT_BUTTON,self.Onbutto,exe3)
	self.Bind(wx.EVT_BUTTON,self.Onbutto,exe4)
	self.Bind(wx.EVT_BUTTON,self.Onbutto,exe5)
	self.Bind(wx.EVT_BUTTON,self.Onbutto,exe6)
        self.Bind(wx.EVT_BUTTON,self.Onbut,but)
        self.Bind(wx.EVT_CLOSE,self.closewindow)
        

    def Onbutton(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Welcomepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def Onbutto(self,event):

        self.Destroy()
	app=wx.PySimpleApp()
        frame=PatientRecordingpage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
               
    

    def Onbut(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Welcomepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def closewindow(self,event):
        self.Destroy()

'''-----------------------------------------------------------------------------#############################################-----------'''
class PatientRecordingpage(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'MESEBONPHY',size=(800,600))
        panel=wx.Panel(self)
	global patient_name
	print patient_name        
	custom=wx.StaticText(panel, -1, " MEMS SENSOR BASED ONLINE PHYSIOTHERAPY ", (200,20),(360,-1), wx.ALIGN_CENTER)
        custo=wx.StaticText(panel, -1, " Welcome " +patient_name+" , Record your exercise ", (200,40),(360,-1), wx.ALIGN_CENTER)
        custom.SetForegroundColour('blue')
        custo.SetForegroundColour('red')
	img1 = wx.Image('arm.jpg', wx.BITMAP_TYPE_ANY)
	sb1 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img1),pos=(50,75))
	img2 = wx.Image('should.jpg', wx.BITMAP_TYPE_ANY)
	sb2 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img2),pos=(50,275))
        
        button=wx.Button(panel,label='Main Menu',pos=(100,500),size=(120,40))
    
        start_rec=wx.Button(panel,label='New Recording',pos=(550,500),size=(120,40))
        but=wx.Button(panel,label='Back',pos=(20,20),size=(80,40))
    
        self.Bind(wx.EVT_BUTTON,self.Onbutton, button)
   
 
        self.Bind(wx.EVT_KEY_DOWN,self.onKeyPress,start_rec)
        self.Bind(wx.EVT_BUTTON,self.record, start_rec)
	#self.Bind(wx.EVT_BUTTON,self.stop, stop_rec)
        self.Bind(wx.EVT_BUTTON,self.Onbut,but)
        self.Bind(wx.EVT_CLOSE,self.closewindow)
	
    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        print keycode
        if keycode == wx.WXK_SPACE:
            print "you pressed the spacebar!"
        event.Skip()

    def Onbutton(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Welcomepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
	'''
    def start(self,event):
        #"""Enable scanning by setting the global flag to True."""
        global flag
        flag = 1
   
    def stop(self,event):
        #"""Stop scanning by setting the global flag to False."""
        global flag
        flag = 0'''    
    def record(self,event):
	global flag
	i=100
	t=time.time()
	s=time.time()
	text_file=open(patient_name +'.txt','w')
	while s-t <10:
		try:	
			x=ser.readline()
	       		print(x) 
			print t-s 
			text_file.write(x)
			if x=="\n":
		   		text_file.seek(0)
				text_file.truncate()
			text_file.flush()
			s=time.time()
		except:
			pass		
		'''try:	
			s=ser.readline().split()
			k=map(float,s)
			print s
			f.write(s)
			f.write('\n')

		except:
			pass'''
        	i=i-1
	text_file.close()

    def Onbut(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Welcomepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def closewindow(self,event):
        self.Destroy()

'''-----------------------------------------------------------------------------#############################################-----------'''
class TherapistRecordingpage(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'MESEBONPHY',size=(800,600))
        panel=wx.Panel(self)       
	custom=wx.StaticText(panel, -1, " MEMS SENSOR BASED ONLINE PHYSIOTHERAPY ", (200,20),(360,-1), wx.ALIGN_CENTER)
        custo=wx.StaticText(panel, -1, " Welcome Doctor , Record your exercise ", (200,40),(360,-1), wx.ALIGN_CENTER)
        custom.SetForegroundColour('blue')
        custo.SetForegroundColour('red')
	img1 = wx.Image('arm.jpg', wx.BITMAP_TYPE_ANY)
	sb1 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img1),pos=(50,75))
	img2 = wx.Image('should.jpg', wx.BITMAP_TYPE_ANY)
	sb2 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img2),pos=(50,275))
        
        button=wx.Button(panel,label='Main Menu',pos=(100,500),size=(120,40))
    
        start_rec=wx.Button(panel,label='New Recording',pos=(550,500),size=(120,40))
        but=wx.Button(panel,label='Back',pos=(20,20),size=(80,40))
    
        self.Bind(wx.EVT_BUTTON,self.Onbutton, button)
   
 
        self.Bind(wx.EVT_KEY_DOWN,self.onKeyPress,start_rec)
        self.Bind(wx.EVT_BUTTON,self.record, start_rec)
	#self.Bind(wx.EVT_BUTTON,self.stop, stop_rec)
        self.Bind(wx.EVT_BUTTON,self.Onbut,but)
        self.Bind(wx.EVT_CLOSE,self.closewindow)
	
    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        print keycode
        if keycode == wx.WXK_SPACE:
            print "you pressed the spacebar!"
        event.Skip()

    def Onbutton(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Welcomepage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
	'''
    def start(self,event):
        #"""Enable scanning by setting the global flag to True."""
        global flag
        flag = 1
   
    def stop(self,event):
        #"""Stop scanning by setting the global flag to False."""
        global flag
        flag = 0'''    
    def record(self,event):
	global flag
	i=100
	t=time.time()
	s=time.time()
	text_file=open('doctor.txt','w')
	while s-t <10:
		try:	
			x=ser.readline()
	       		print(x) 
			print t-s 
			text_file.write(x)
			if x=="\n":
		   		text_file.seek(0)
				text_file.truncate()
			text_file.flush()
			s=time.time()
		except:
			pass		
		'''try:	
			s=ser.readline().split()
			k=map(float,s)
			print s
			f.write(s)
			f.write('\n')

		except:
			pass'''
        	i=i-1
	text_file.close()

    def Onbut(self,event):

        self.Destroy()
        app=wx.PySimpleApp()
        frame=Therapistpage(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
        
    def closewindow(self,event):
        self.Destroy()

'''-----------------------------------------------------------------------------#############################################-----------'''

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=Welcomepage(parent=None,id=-1)
    frame.Show()
    app.MainLoop()

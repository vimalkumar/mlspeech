#!/usr/bin/python
print "importing libraries..."
import numpy, pylab
print "DONE"

class ECG:

    def trim(self, data,degree=100):
        print 'trimming'
        i,data2=0,[]
        while i<len(data):
            data2.append(sum(data[i:i+degree])/degree)
            i+=degree
        return data2

    def smooth(self,list,degree=15):
        mults=[1]
        s=[]
        for i in range(degree): mults.append(mults[-1]+1)
        for i in range(degree): mults.append(mults[-1]-1)
        for i in range(len(list)-len(mults)):
            small=list[i:i+len(mults)]
            for j in range(len(small)):
                small[j]=small[j]*mults[j]
            val=sum(small)/sum(mults)
            s.append(val)
        return s

    def smoothWindow(self,list,degree=10):
        list2=[]
        for i in range(len(list)):
            list2.append(sum(list[i:i+degree])/float(degree))
        return list2

    def invertYs(self):
        print 'inverting'
        self.ys=self.ys*-1

    def takeDeriv(self,dist=5):
        print 'taking derivative'
        self.dys=[]
        for i in range(dist,len(self.ys)):
            self.dys.append(self.ys[i]-self.ys[i-dist])
        self.dxs=self.xs[0:len(self.dys)]

    def genXs(self, length, hz):
        print 'generating Xs'
        step = 1.0/(hz)
        xs=[]
        for i in range(length): xs.append(step*i)
        return xs

    def loadFile(self, fname, startAt=None, length=None, hz=1000):
        print 'loading',fname
        self.ys = numpy.memmap(fname, dtype='h', mode='r')*-1
        print 'read %d points.'%len(self.ys)
        self.xs = self.genXs(len(self.ys),hz)
        if startAt and length:
            self.ys=self.ys[startAt:startAt+length]
            self.xs=self.xs[startAt:startAt+length]

ys = numpy.memmap("vowels.wav", dtype=numpy.int16, mode='r')

    def findBeats(self):
        print 'finding beats'
        self.bx,self.by=[],[]
        for i in range(100,len(self.ys)-100):
            if self.ys[i]<15000: continue # SET THIS VISUALLY
            if self.ys[i]<self.ys[i+1] or self.ys[i]<self.ys[i-1]: continue
            if self.ys[i]-self.ys[i-100]>5000 and self.ys[i]-self.ys[i+100]>5000:
                self.bx.append(self.xs[i])
                self.by.append(self.ys[i])
        print "found %d beats"%(len(self.bx))

    def genRRIs(self,fromText=False):
        print 'generating RRIs'
        self.rris=[]
        if fromText: mult=1
        else: 1000.0
        for i in range(1,len(self.bx)):
            rri=(self.bx[i]-self.bx[i-1])*mult
            #if fromText==False and len(self.rris)>1:
                #if abs(rri-self.rris[-1])>rri/2.0: continue
            #print i, "%.03f\t%.03f\t%.2f"%(bx[i],rri,60.0/rri)
            self.rris.append(rri)

    def removeOutliers(self):
        beatT=[]
        beatRRI=[]
        beatBPM=[]
        for i in range(1,len(self.rris)):
            if self.rris[i]<0.5 or self.rris[i]>1.1: continue #CHANGE THIS AS NEEDED 
            if abs(self.rris[i]-self.rris[i-1])>self.rris[i-1]/5: continue
            beatT.append(self.bx[i])
            beatRRI.append(self.rris[i])
        self.bx=beatT
        self.rris=beatRRI
            
    def graphTrace(self):
        pylab.plot(self.xs,self.ys)
        #pylab.plot(self.xs[100000:100000+4000],self.ys[100000:100000+4000])
        pylab.title("Electrocardiograph")
        pylab.xlabel("Time (seconds)")
        pylab.ylabel("Potential (au)")

    def graphDeriv(self):
        pylab.plot(self.dxs,self.dys)
        pylab.xlabel("Time (seconds)")
        pylab.ylabel("d/dt Potential (au)")

    def graphBeats(self):
        pylab.plot(self.bx,self.by,'.')
        
    def graphRRIs(self):
        pylab.plot(self.bx,self.rris,'.')
        pylab.title("Beat Intervals")
        pylab.xlabel("Beat Number")
        pylab.ylabel("RRI (ms)")

    def graphHRs(self):
        #HR TREND
        hrs=(60.0/numpy.array(self.rris)).tolist()
        bxs=(numpy.array(self.bx[0:len(hrs)])/60.0).tolist()
        pylab.plot(bxs,hrs,'g',alpha=.2)
        hrs=self.smooth(hrs,10)
        bxs=bxs[10:len(hrs)+10]
        pylab.plot(bxs,hrs,'b')
        pylab.title("Heart Rate")
        pylab.xlabel("Time (minutes)")
        pylab.ylabel("HR (bpm)")

    def graphPoincare(self):
        #POINCARE PLOT
        pylab.plot(self.rris[1:],self.rris[:-1],"b.",alpha=.5)
        pylab.title("Poincare Plot")
        pylab.ylabel("RRI[i] (sec)")
        pylab.xlabel("RRI[i+1] (sec)")

    def graphFFT(self):
        #PSD ANALYSIS
        fft=numpy.fft.fft(numpy.array(self.rris)*1000.0)
        fftx=numpy.fft.fftfreq(len(self.rris),d=1)
        fftx,fft=fftx[1:len(fftx)/2],abs(fft[1:len(fft)/2])
        fft=self.smoothWindow(fft,15)
        pylab.plot(fftx[2:],fft[2:])
        pylab.title("Raw Power Sprectrum")
        pylab.ylabel("Power (ms^2)")
        pylab.xlabel("Frequency (Hz)")
		
    def graphFFT2(self):
        #PSD ANALYSIS
        fft=numpy.fft.fft(numpy.array(self.rris)*1000.0)
        fftx=numpy.fft.fftfreq(len(self.rris),d=1)
        fftx,fft=fftx[1:len(fftx)/2],abs(fft[1:len(fft)/2])
        fft=self.smoothWindow(fft,15)
        for i in range(len(fft)):
            fft[i]=fft[i]*fftx[i]
        pylab.plot(fftx[2:],fft[2:])
        pylab.title("Power Sprectrum Density")
        pylab.ylabel("Power (ms^2)/Hz")
        pylab.xlabel("Frequency (Hz)")

    def graphHisto(self):
        pylab.hist(self.rris,bins=20,ec='none')
        pylab.title("RRI Deviation Histogram")
        pylab.ylabel("Frequency (count)")
        pylab.xlabel("RRI (ms)")
        #pdf, bins, patches = pylab.hist(self.rris,bins=100,alpha=0)
        #pylab.plot(bins[1:],pdf,'g.')
        #y=self.smooth(list(pdf[1:]),10)
        #x=bins[10:len(y)+10]
        #pylab.plot(x,y)

    def saveBeats(self,fname):
        print "writing to",fname
        numpy.save(fname,[numpy.array(self.bx)])
        print "COMPLETE"

    def loadBeats(self,fname):
        print "loading data from",fname
        self.bx=numpy.load(fname)[0]
        print "loadded",len(self.bx),"beats"
        self.genRRIs(True)


def snd2txt(fname):
    ## SND TO TXT ##
    a=ECG()
    a.loadFile(fname)#,100000,4000)
    a.invertYs()
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphTrace()
    a.findBeats()
    a.graphBeats()
    a.saveBeats(fname)
    pylab.show()

def txt2graphs(fname):
    ## GRAPH TXT ##
    a=ECG()
    a.loadBeats(fname+'.npy')
    a.removeOutliers()
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphHRs();pylab.subplots_adjust(left=.1,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_Heart_Rate_Over_Time.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphFFT();pylab.subplots_adjust(left=.13,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_Power_Spectrum_Raw.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphFFT2();pylab.subplots_adjust(left=.13,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_Power_Spectrum_Weighted.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphPoincare();pylab.subplots_adjust(left=.1,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_Poincare_Plot.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphRRIs();pylab.subplots_adjust(left=.1,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_RR_Beat_Interval.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphHisto();pylab.subplots_adjust(left=.1,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_RR_Deviation_Histogram.png");
    pylab.show();

fname='ecg.wav'
raw_input("\npress ENTER to analyze %s..."%(fname))
snd2txt(fname)
raw_input("\npress ENTER to graph %s.npy..."%(fname))
txt2graphs(fname)

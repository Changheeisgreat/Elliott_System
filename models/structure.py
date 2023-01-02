


'''
log_label update -> structure update 
and then ... 
always react to identifier 
'''

class structure:
    def __init__(self):
        self.price=list()
        self.label=list()
        
        self.monowave=dict() #groupwave
        self.logic=dict() #key : groupmonowave index int
                          #value : rule-condition tuple    
        
    def structure_labeling(self,idx):
        idx # groupmonowave index 
        logic=self.logic[idx]
        #page 124 


        #idx-2 : m-1 
        #idx-1 : m0
        #idx   : m1 
        #idx+1 : m2

        if logic[0] =='1a':
            if any([self.l(idx+1)>=self.l(idx),
                    self.l(idx+1)>=self.l(idx+2)]):
                logic+(':5',)
            if all([self.c(idx-2)>=1.00*self.r(idx-1),
                      self.c(idx-2)<=1.618*self.r(idx-1),
                      self.c(idx-1)==self.r(idx), #similar how I code it?
                      self.p(idx+3,'e')<=self.p(idx-1,'e')]):
                logic+(':s5',)
            if all([self.n(idx-1)>=3,
                    self.l(idx-1)>=self.l(idx),
                    self.r(idx)>self.c(idx-1)]):
                logic+('*',)



        if logic[0] =='1b':
            if all([self.c(idx-2)>self.r(idx-1)*1.00,
                    self.c(idx-2)>self.r(idx-1)*1.618,
                    self.cmp(idx,idx-1,idx+3)]):
                logic+(':s5',) 
                self.logic[idx+1]+('x:c3?')
            if all([self.n(idx)>=3,
                    self.l(idx)<self.l(idx-1),
                    self.r(idx)>self.c(idx-1)]):
                logic+('*',)
            if all([self.btw(idx,idx-1,idx+1),
                    self.l(idx+2)<=self.l(idx),
                    self.c(idx+2)>=self.c(idx),
                    self.c(idx-2)>self.c(idx)]):
                logic+(':sL3')
            if all([self.btw(idx,idx-1,idx+1),
                    self.l(idx+2)<=self.l(idx),
                    self.c(idx+2)>=self.c(idx),
                    self.c(idx-1)<self.c(idx),]):  #hell +++
                logic+(':c3')
            if all([self.c(idx+2)<self.c(idx),
                    self.btw(idx,idx-1,idx+1),
                    self.c(idx-2)>self.c(idx-1),
                    any([self.c(idx)>self.c(idx-2),
                         self.c(idx+2)>self.c(idx)])]): #hell +++
                logic+(':c3')
            else:
                logic+(':5',)
        if logic[0]=='1c':
            logic+(':5',)
            if all([self.p(idx-1,'e')==self.p(idx,'e'),
                    ]):
                pass

        if logic[0]=='1d':
            logic+(':5')
        
        if logic[0]=='2a':
            logic=logic+(':5')
            if all([self.cmp(idx,idx-1,idx+3)]):
                logic=logic+(':s5')
                #logic=self.logic[idx] 
                #self.logic[idx+1]=self.logic[idx+1]+('x:c3?')
            if all([any([self.c(idx)>self.c(idx-2),
                        self.c(idx)>self.c(idx+2)]),
                    self.size([self.c(idx-2),self.c(idx),self.c(idx+2)]),
                    self.r(idx+2)>self.c(idx+1)*0.618]):
                logic=logic+('*m1 is 3 *')
            if all([self.n(idx-1)>=3,
                    self.l(idx)<=self.l(idx-1),
                    self.c(idx)>=self.c(idx-1)]):   
                logic=logic+('l')
            if all([self.c(idx-2)>=self.c(idx)*1.618,
                    self.l(idx+2)<=self.l(idx-2),
                    self.c(idx+2)>self.c(idx-2),]): 
                # what is 61.8% between m0 and m2 for about time and price ??
                logic=logic+('[:c3]')
            # p 128 ????? fifth if..
            if all([self.c(idx-2)>self.c(idx-1),
                    self.c(idx-1)<self.c(idx),
                    min([self.c(idx-2),self.c(idx),self.c(idx+2)])!=self.c(idx),
                    self.l(idx+3)>=self.l(idx+2),
                    self.r(idx+3)>self.c(idx+2)]):
                logic=logic+(':c3')

        if logic[0]=='2b':
            pass
        if logic[0]=='2c':
            pass
        if logic[0]=='2d':
            pass
        if logic[0]=='3a':
            pass
        if logic[0]=='3b':
            pass
        if logic[0]=='3c':
            pass
        if logic[0]=='3d':
            pass
        if logic[0]=='3e':
            pass
        if logic[0]=='3f':
            pass
        if logic[0]=='4ai':
            pass
        if logic[0]=='4aii':
            pass
        if logic[0]=='4aiii':
            pass
        if logic[0]=='4bi':
            pass
        if logic[0]=='4bii':
            pass
        if logic[0]=='4biii':
            pass
        if logic[0]=='4ci':
            pass
        if logic[0]=='4cii':
            pass
        if logic[0]=='4ciii':
            pass
        if logic[0]=='4di' or logic[0]=='4dii':
            pass
        if logic[0]=='4diii':
            pass
        if logic[0]=='4dei' or logic[0]=='4eii':
            pass
        if logic[0]=='4eiii':
            pass
        if logic[0]=='5a':
            pass
        if logic[0]=='5b':
            pass
        if logic[0]=='5c':
            pass
        if logic[0]=='5d':
            pass
        if logic[0]=='6a':
            pass
        if logic[0]=='6b':
            pass
        if logic[0]=='6c':
            pass
        if logic[0]=='6d':
            pass
        if logic[0]=='7a':
            pass
        if logic[0]=='7b':
            pass
        if logic[0]=='7c':
            pass
        if logic[0]=='7d':
            pass



            
        print('u can do it ')

    def btw(self,idx,idx_a,idx_b):
        if self.c(idx)>0:
            return self.p(idx_a,'s')>self.p(idx_b,'e')
        if self.c(idx)<0:
            return self.p(idx_a,'e')>self.p(idx_b,'s')

    def cmp(self,idx,idx_a,idx_b): #compare end prices 
        if self.c(idx)>0:
            return self.p(idx_b,'e')>self.p(idx_a,'e')
        elif self.c(idx)<0:
            return self.p(idx_b,'e')<self.p(idx_a,'e')

    def n(self,idx): #num of label(M1,M2,M3) in the monowave (MG1)
        labelset=self.label[self.monowave[idx][0]:self.monowave[idx][-1]+1]
        return len(set(labelset))

    def p(self,idx,param='e'): #price of endpoint or startpoint
        if param=='e':
            output=self.price[self.monowave[idx]-1]
        elif param=='s':
            output=self.price[self.monowave[idx][0]-1]
        return output

    def l(self,idx): #index length #len(M)-1 : time pass 
        return len(self.monowave[idx])-1
    
    def c(self,idx): #price change
        start_idx=self.monowave[idx][0]
        end_idx=self.monowave[idx][-1]
        start_price=self.price[start_idx-1]
        end_price=self.price[end_idx-1]
        return end_price-start_price

    def r(self,idx): #price return 
        end_idx=self.monowave[idx][-1]
        new_idx=end_idx+1             #new_idx=self.log_index[i+1]-1
        end_price=self.price[end_idx-1]
        new_price=self.price[new_idx]
        return new_price-end_price

    @staticmethod
    def size(list):
        a=max(list)
        b=min(list)
        list.remove(b)
        c=min(list)
        return a>c
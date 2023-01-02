import os 
'''
elliott.py 
identifier.price=mon.price
identifier.monowave=mon.group_wave 
what if new groupwave's number is more than 1 how u can deal with this??? 
make stack... 
identifier()
'''
class identifier:
    def __init__(self):
        self.price=list()
        self.monowave=dict()
        self.logic=dict()    #keys:monowave key index
                             #values:label of tuple
        self.cur_idx=None

    def add(self,data):
        self.price.append(data)

    def startidx(self):
        if len(self.price)==30:
            idx=self.price.index(min(self.price))
            for i in range(len(self.monowave)):
                if idx in self.monowave[i]:
                    break
            self.cur_idx=i+1
        else: 
            pass

    def rule_identifier(self,mono_idx):
        self.idx=mono_idx

        start_idx=self.monowave[self.idx][0]
        end_idx=self.monowave[self.idx][-1]
        new_idx=end_idx+1

        start_price=self.price[start_idx-1]
        end_price=self.price[end_idx-1]
        new_price=self.price[new_idx]

        mono_change=abs(end_price-start_price)
        mono_return=abs(new_price-end_price)

        if mono_return<mono_change*0.382:
            self.rule=1
        elif mono_return<mono_change*0.618 and mono_return>mono_change*0.382:
            self.rule=2
        elif mono_return==mono_change*0.618:
            self.rule=3
        elif mono_return<mono_change*1.00 and mono_return>mono_change*0.618:
            self.rule=4
        elif mono_return<mono_change*1.618 and mono_return>mono_change*1.00:
            self.rule=5
        elif mono_return<mono_change*2.618 and mono_return>mono_change*1.618:
            self.rule=6
        elif mono_return>mono_change*2.618:
            self.rule=7
        

    def condition_identifier(self):
        #current monowave m_x
        start_idx=self.monowave[self.idx][0]
        end_idx=self.monowave[self.idx][-1]    
        start_price=self.price[start_idx-1]
        end_price=self.price[end_idx-1]
        #prior monowave m_x-1
        start_idx_f=self.monowave[self.idx-1][0]
        end_idx_f=self.monowave[self.idx-1][-1]  
        start_price_f=self.price[start_idx_f]
        end_price_f=self.price[end_idx_f]

        mono_return=abs(end_price-start_price)
        mono_change=abs(end_price_f-start_price_f)

        proportion=mono_return/mono_change

        if proportion < 0.382:
            self.precon='a'
        elif proportion < 0.618 and proportion >= 0.382:
            self.precon='b'
        elif proportion < 1.000 and proportion >= 0.618:
            self.precon='c'
        elif proportion < 1.618 and proportion >= 1.000:
            self.precon='d1'
        elif proportion == 1.618:
            self.precon='d2'
        elif proportion <= 2.618 and proportion > 1.618:
            self.precon='e'
        elif proportion > 2.618:
            self.precon='f'

    def precon_to_con(self):
        
        #rule 1
        if self.rule==1:
            if any([self.precon=='a',self.precon=='b']):
                self.condition='a'
            elif self.precon=='c':
                self.condition='b'
            elif any([self.precon=='d1',self.precon=='d2']):
                self.condition='c'
            elif any([self.precon=='e',self.precon=='f']):
                self.condition='d'
        #rule 2
        elif self.rule==2:
            if self.precon=='a':
                self.condition='a'
            elif self.precon=='b':
                self.condition='b'
            elif self.precon=='c':
                self.condtion='c'
            elif any([self.precon=='d1',self.precon=='d2']):
                self.condition='d'
            elif any([self.precon=='e',self.precon=='f']):
                self.condition='e'
        #rule 3
        elif self.rule==3:
            if self.precon=='a':
                self.condition='a'
            elif self.precon=='b':
                self.condition='b'
            elif self.precon=='c':
                self.condtion='c'
            elif self.precon=='d1':
                self.condition='d'
            elif any([self.precon=='d2',self.precon=='e']):
                self.condition='e'
            elif self.precon=='f':
                self.condition='f'
        #rule 4
        elif self.rule==4:
            if self.precon=='a':
                self.condition='a'
            elif any([self.precon=='b',self.precon=='c']):
                self.condition='b'
            elif self.precon=='d1':
                self.condition='c'
            elif any([self.precon=='d2',self.precon=='e']):
                self.condition='d'
            elif self.precon=='f':
                self.condition='e'
            self.category_identifier()

        #rule 5, rule 6, rule 7
        elif any([self.rule==5,self.rule==6,self.rule==7]):
            if any([self.precon=='a',self.precon=='b',self.precon=='c']):
                self.condition='a'
            elif self.precon=='d1':
                self.condition='b'
            elif any([self.precon=='d2',self.precon=='e']): 
                self.condition='c'
            elif self.precon=='f': 
                self.condition='d'
        
        self.logic[self.cur_idx]=tuple((str(self.rule)+self.condition),)

    def category_identifier(self):
        start_idx=self.monowave[self.idx+1][0]
        end_idx=self.monowave[self.idx+1][-1]
        new_idx=end_idx+1

        start_price=self.price[start_idx-1]
        end_price=self.price[end_idx-1]
        new_price=self.price[new_idx]

        mono2_change=abs(end_price-start_price)
        mono3_return=abs(new_price-end_price)

        if mono3_return>=mono2_change*1.00 and mono3_return<mono2_change*1.618:
            self.condition+'i'
        elif mono3_return>=mono2_change*1.618 and mono3_return<=mono2_change*2.618:
            self.condition+'ii'
        elif mono3_return>mono2_change*2.618:
            self.condition+'iii'


    def __call__(self):
        if len(self.price) >= 30:
            self.startidx()

            if self.monowave.get(self.cur_idx+5):
                self.rule_identifier(self.cur_idx)
                self.condition_identifier()
                self.precon_to_con()
                self.cur_idx+=1

                # return last key and item add to the class 
                print(self.logic)
            else:
                pass
        else:
            pass
        
    
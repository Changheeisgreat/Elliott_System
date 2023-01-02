# wave detector classses
import os
import math
import warnings
warnings.filterwarnings("ignore")

import numpy as np

class monowave:
    def __init__(self):
        #initial settings and outputs
        self.idx=1
        self.status=str()
        self.price=list()
        self.label=list()

        #switchs
        self.rule_of_proportion_switch=bool()
        self.rule_of_neurality_switch=bool()
        self.rule_of_observation_switch=bool()

        #parameters
        self.timestamp=float(86400)
        self.ratio=float(10/86400)
        self.ptr=self.timestamp *self.ratio

        #output
        self.log_index=list() # list for price index of log_label
        self.log_label=list() # list for unique price label
        self.direction=dict()
        self.group_monowave=dict()
        self.newline=list()
        #temporal

        self.stop=True
        self.tmp_r_ob=dict()

    def add(self,price):
        self.price.append(price)

    #indexing monowaves as M1 M2 M3 M4 ...
    #at this time we do not mind the direction
    #analyze function starts when length is over 3

    def mono_indexing(self):

        if len(self.price)<3:
            self.rule_of_proportion_switch=False
            label='M'+str(self.idx)

            if self.price[0]<self.price[-1]:
                self.status='inc'
            else:
                self.status='dec'

        else:
            self.rule_of_proportion_switch=True
            # keep increasing
            if self.status=='inc':
                if self.price[-2]<=self.price[-1]:
                    label='M'+str(self.idx)
                    self.rule_of_neurality_switch=False
                else:
                    self.idx+=1
                    label='M'+str(self.idx)
                    self.status='dec'
                    self.rule_of_neurality_switch=True

            elif self.status=='dec':
                if self.price[-2]<=self.price[-1]:
                    self.idx+=1
                    label='M'+str(self.idx)
                    self.status='inc'
                    self.rule_of_neurality_switch=True
                else:
                    label='M'+str(self.idx)
                    self.rule_of_neurality_switch=False

        self.label.append(label)

        return label

    def logger(self,label):
        '''
        find changing moments
        '''
        if label not in self.log_label:
            self.log_label.append(label)
            self.log_index.append(len(self.price))
            if len(self.log_label)>=2:
                self.rule_of_observation_switch=True
        else:
            self.rule_of_observation_switch=False

    def group_wave_encoding(self,start,end):
        # start and new is index number
        #print('start : {} end: {}'.format(start,end) )
        if start==end:
            end+=1
        idx_li=[x for x in range(start,end)]

        #print('this is start : {} and new : {}'.format(start,new))
        self.group_monowave[self.group_idx]=idx_li
        self.group_idx+=1
        self.tmp_r_ob=dict()
        print('{} : current group wave index elements is : {} '.format(self.group_idx-1,self.group_monowave[self.group_idx-1]))

    def rule_of_proportion(self):
        '''
        self.log_label : unique label
        self.log_index -1 : the index of label

        todo
        alternate fot syntax as window size approach.
        '''

        for i in range(len(self.log_label)-1):
            start_idx=self.log_index[i]-1
            new_idx=self.log_index[i+1]-1
            start_price=self.price[start_idx]
            end_price=self.price[new_idx-1]
            new_price=self.price[new_idx]

            mono_change=end_price-start_price
            mono_return=new_price-end_price

            self.mono618=0.618*abs(mono_change)

            # price change
            t_pass=(new_idx-1)-start_idx
            base_t=t_pass*self.ptr
            angle=round(math.degrees(math.atan(abs(mono_change)/base_t)),0)

            upper_limit=end_price*1.25-start_price
            lower_limit=base_t*1.25

            upper_angle=round(math.degrees(math.atan(abs(upper_limit)/base_t)),0)
            lower_angle=round(math.degrees(math.atan(abs(mono_change)/lower_limit)),0)

            if self.mono618<abs(mono_return):
                if angle<upper_angle or angle>lower_angle:
                    for key in range(start_idx,new_idx):
                        self.direction.update({key:'Dir'})

                self.direction.update({new_idx:'Non-Dir'})

            else:
                if angle<upper_angle or angle>lower_angle:
                    for key in range(start_idx,new_idx):
                        self.direction.update({key:'Dir'})

                self.direction.update({new_idx:'Dir'})

    def rule_of_neurality(self,label):
        '''
        only activate when direction changed.
        find the prior index and price
        change the label if it is under 45
        '''

        #idx=self.log_label.index(label)
        #new_idx=self.log_index[idx]-1
        new_idx=len(self.price)-1
        new_price=self.price[new_idx]
        end_price=self.price[new_idx-1]
        change=new_price-end_price

        angle=round(math.degrees(math.atan(abs(change)/self.ptr)),0)

        if angle <45:
            #rollback
            print('rollback!')

            self.log_label.pop()
            self.log_index.pop()
            self.label.pop()
            self.label.append(self.log_label[-1])
            self.idx-=1
            self.rule_of_observation_switch=False
            if self.status =='dec':
                self.status = 'inc'
            elif self.status =='inc':
                self.status ='dec'
        #todo
        #exception handling
        # if neuralityisOn=True:

    def preset_r_ob(self):
        # it has to be excuted just one time for whole loop
        if len(self.log_label)==2:
            if self.stop:
                start=0
                end=len(self.label)-1

                self.group_idx=0
                self.group_wave_encoding(start,end)
                self.stop=False
            else:
                pass
        else:
            pass

    def rule_of_observation(self):
        '''
        first : set the initial group monowaves
        second : set two prices of the start and the end of group monowave
        third : if new price broke the either point then integrate monowaves
        '''
        if self.group_idx<2:
            start_index=self.group_monowave[self.group_idx-1][0]
            start_price=self.price[start_index]
            end_index=self.group_monowave[self.group_idx-1][-1]
            end_price=self.price[end_index]
        else:
            start_index=self.group_monowave[self.group_idx-2][-1]
            start_price=self.price[start_index]
            end_index=self.group_monowave[self.group_idx-1][-1]
            end_price=self.price[end_index]
        #start_price and end_price : #mx[0], mx[-1]
        #self.log_index[-1]-1 : small monowave x+2 start index
        #self.log_index[-1]-2 : small monowave x+1 end index
        # if pass -> x+=1


        mono_end_price=self.price[self.log_index[-1]-2]
        #print('monogram{} endprice is {}'.format(self.label[-2],mono_end_price))
        if start_price-end_price<0: # mono increased
            if mono_end_price>start_price and mono_end_price<end_price:
                pass
            elif mono_end_price<start_price:
                #new price : firstly inputted monowave's first price index
                #end price: lastly inputted monowave's end price index
                new_start_index=end_index+1
                new_end_index=self.log_index[-1]-1

                self.group_wave_encoding(new_start_index,new_end_index)
                ##print(new_start_index,new_end_index)


            elif mono_end_price>end_price:
            #    new price : firstly inputted monowave's first price index
            #    end price : minimum point of monowave index
                new_start_index=end_index+1
                new_end_index=self.tmp_r_ob[min(list(self.tmp_r_ob.keys()))]+1

                self.group_wave_encoding(new_start_index,new_end_index)
            #    new price 2: after point of end price index
            #    end price 2: lastly inpuuted monowave's end price index]
                new_start_index2=new_end_index
                new_end_index2=self.log_index[-1]-1

                self.group_wave_encoding(new_start_index2,new_end_index2)

        elif start_price-end_price>0: # mono decreased
            if mono_end_price<start_price and mono_end_price>end_price:
                pass
            elif mono_end_price>start_price:
                #new price : firstly inputted monowave's first price index
                #end price: lastly inputted monowave's end price index
                new_start_index=end_index+1
                new_end_index=self.log_index[-1]-1

                self.group_wave_encoding(new_start_index,new_end_index)

            elif mono_end_price<end_price:
            #    new price : firstly inputted monowave's first price index
            #    end price : minimum point of monowave index
                new_start_index=end_index+1
                new_end_index=self.tmp_r_ob[max(list(self.tmp_r_ob.keys()))]+1

                self.group_wave_encoding(new_start_index,new_end_index)
            #    new price 2: after point of end price index
            #    end price 2: lastly inpuuted monowave's end price index]
                new_start_index2=new_end_index
                new_end_index2=self.log_index[-1]-1

                self.group_wave_encoding(new_start_index2,new_end_index2)

    def groupwave_line(self):
        st=np.linspace(self.price[self.group_monowave[0][0]],
                self.price[self.group_monowave[0][-1]],
                len(self.group_monowave[0]))

        for i in range(len(self.group_monowave)-1):
            new=np.linspace(self.price[self.group_monowave[i][-1]],
                    self.price[self.group_monowave[i+1][-1]],
                    len(self.group_monowave[i+1])+1)[1:]
            st=np.append(st, new)
        return st.tolist()

    def analyze(self):
        label=self.mono_indexing()
        self.direction[len(self.price)-1]=None
        self.logger(label)

        if self.rule_of_proportion_switch:
            self.rule_of_proportion()

        if self.rule_of_neurality_switch:
            self.rule_of_neurality(label)

        self.preset_r_ob()
        if len(self.log_label)>2:
            mono_end_price=self.price[self.log_index[-1]-2]
            self.tmp_r_ob[mono_end_price]=self.log_index[-1]-2
            if self.rule_of_observation_switch:
                self.rule_of_observation()
                self.newline=self.groupwave_line()

        #write logs
        os.makedirs('models/logs',exist_ok=True)
        cwd=os.getcwd()+'/models/logs'
        filename = os.path.join(cwd, 'log.txt')
        with open(filename,'a') as f:
            f.write("%s, %s \n"%(self.price[-1],self.label[-1]))

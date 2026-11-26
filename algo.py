import math

from interval_sets import Interval, IntervalSet

import random

vis = True
if vis: from visual import plot_interval_sets 


def raspr_dyn_without_smych(dlit: list, start: IntervalSet = IntervalSet([Interval(0,0)]), end: IntervalSet = IntervalSet([Interval(-1000,1000)]), were_can_be: IntervalSet = IntervalSet([Interval(0,100000)]), vs: Interval = Interval(50,100)) -> list: 

    l = []     # дин. список куда для каждого i записываются значения с которых нота может стартовать, i+1 - куда может прийти
                                            # start под 0 номером, end должен дать непустое пересечение с номером len(dlit)

    l.append(start)



    print(type(l))

    for dl in dlit:    #проход туда - понимаем прошли/не прошли, но не помним как. Помним зависимость только в одном направлении
        start_intervals=l[-1]                # т.е. для каждой точки здесь записываются те интервалы в коотрые мы можем прийти со старта
        new_intervals = []
        for interval in start_intervals:
            new_intervals.append(Interval(interval.start-vs.end*dl,interval.end-vs.start*dl))
            new_intervals.append(Interval(interval.start+vs.start*dl,interval.end+vs.end*dl))
                            
        print('-', IntervalSet(new_intervals), dl)
        l.append(IntervalSet([IntervalSet(new_intervals) & were_can_be]))
        print(l[-1])

    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()


    if l[-1] & end:                            # а это проход обратно - и тут мы уже выбираем те точки, с которых можно дойти до конца - и сразу на каждом шагу выбираем из них только те, в которые можно дойти от начала (по уже существующим в списке интервалам)
        l[-1] = IntervalSet( [l[-1] & end])                    # таким образом у нас получается список, где мы в каждой точке есть положение, в которое гарантированно можно поставить смычок и начать играть в любую сторону - и всё будет хорошо
        for i in range(len(l)-1, 0, -1):
            dl = dlit[i-1]
            end_intervals=l[i]
            new_intervals = []
            for interval in end_intervals:
                new_intervals.append(Interval(interval.start-vs.end*dl,interval.end-vs.start*dl))
                new_intervals.append(Interval(interval.start+vs.start*dl,interval.end+vs.end*dl))
                                
            print('-', IntervalSet(new_intervals), dl)
            print(l[i-1])   
            l[i-1]=IntervalSet([IntervalSet(new_intervals) & l[i-1]])
            print(l[i-1])    





    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()




    def randFromIntervalSet(my_IntervalSet):
        chosen_interval = random.choice(list(my_IntervalSet))                   # я пока не прописала и не знаю по какому принципу выбирать, поэтому пусть будет рандом
        return random.randint(int(chosen_interval.start), int(chosen_interval.end))

    if l[-1] and l[0]:

        a = []  #массив, куда запишется то что нам надо для сценария из этой прелести, нумерация согласно dlit
        p = [randFromIntervalSet(start)]  #массив уже выбранных положений, нумерация согласно l

        for i in range(len(dlit)):
            dl=dlit[i]
            start_p = p[-1]
            new_intervals = IntervalSet([l[i+1] & (Interval(start_p-vs.end*dl,start_p-vs.start*dl) | Interval(start_p+vs.start*dl,start_p+vs.end*dl))])

            
            p_predvarit = randFromIntervalSet(new_intervals)     # я пока не прописала и не знаю по какому принципу выбирать, поэтому пусть будет рандом

            v = round((p_predvarit-start_p)/dl)
            p.append(start_p+v*dl) 

            if not p[-1] in new_intervals:     # проверка на случай если при округлении скорости у нас точка вылезла за интервал. Мне было лень её прописывать нормально, так что придётся читать как есть
                v+=1
                pn=start_p+v*dl
                if not pn in new_intervals:
                    v-=2
                    pn=start_p+v*dl
                    if not pn in new_intervals:
                        v+=1
                        pn=p[-1]
                        print('Ой, а вот и то самое бутылоное горлышко, осторожно')
                p[-1]=pn


            a.append((int(v>0), dl, abs(v)))

            print(a[-1])

        return a

def raspr_dyn_with_smych(dlit: list, indices, start: IntervalSet = IntervalSet([Interval(0,0)]), end: IntervalSet = IntervalSet([Interval(-1000,1000)]), were_can_be: IntervalSet = IntervalSet([Interval(0,100000)]), vs: Interval = Interval(50,100)) -> list: 

    # индексы длительностей перед которыми нужна смена смычка
    if 0 in indices: indices.remove(0)

    start = IntervalSet([Interval(0,0)])

    end = IntervalSet([Interval(-1000,1000)])

    l1 = []     # дин. списки куда для каждого i записываются значения с которых нота может стартовать, i+1 - куда может прийти
    l0 = []                                         # start под 0 номером, end должен дать непустое пересечение с номером len(dlit)

    l1.append(start)                    # в l1 мы записываем те значения в которые пришли в + направлении
    l0.append(start)                    # в l0 - те в которые пришли в отрицательном направлении

    #were_can_be = IntervalSet([Interval(0,100000)])
    #vs = Interval(48,133)


    for i in range(len(dlit)):    #проход туда - понимаем прошли/не прошли, но не помним как. Помним зависимость только в одном направлении
        dl = dlit[i]                                   # т.е. для каждой точки здесь записываются те интервалы в коотрые мы можем прийти со старта
        
        if i in indices: start_intervals=l1[-1]          #сначала считаем для l0 - для них при необходимости смены смычка нам нужны предыдущие значения из l1
        else: start_intervals=IntervalSet([l1[-1]|l0[-1]]) 
        new_intervals = []
        for interval in start_intervals:
            new_intervals.append(Interval(interval.start-vs.end*dl,interval.end-vs.start*dl))
        print('-', IntervalSet(new_intervals), dl)
        l0.append(IntervalSet([IntervalSet(new_intervals) & were_can_be]))
        print(l0[-1])

        if i in indices: start_intervals=l0[-2]          #затем для l1 - здесь уже поменялся индекс у l0, т.к. мы в него кое-что добавили только что
        else: start_intervals=IntervalSet([l1[-1]|l0[-2]])
        new_intervals = []
        for interval in start_intervals:
            new_intervals.append(Interval(interval.start+vs.start*dl,interval.end+vs.end*dl))
        print('-', IntervalSet(new_intervals), dl)
        l1.append(IntervalSet([IntervalSet(new_intervals) & were_can_be]))
        print(l1[-1])


    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()



    if IntervalSet([(l1[-1]|l0[-1])]) & end:                            # а это проход обратно - и тут мы уже выбираем те точки, с которых можно дойти до конца - и сразу на каждом шагу выбираем из них только те, в которые можно дойти от начала (по уже существующим в списке интервалам)
        l1[-1] = IntervalSet( [l1[-1] & end])                    # таким образом у нас получается список, где мы в каждой точке есть положение, в которое гарантированно можно поставить смычок и начать играть в любую сторону - и всё будет хорошо
        l0[-1] = IntervalSet( [l0[-1] & end])                    # кстати теперь l1 у нас выполняет функцию куда мы дошли с конца в положительном направлении
        for i in range(len(l1)-1, 0, -1):                           # l0 - напротив функцию того, откуда можно пойти в положительном и достигнуть конца
            dl = dlit[i-1]
            print()
            l_old_start = IntervalSet([l0[i-1]|l1[i-1]])
            if i in indices: 
                print('+')
                end_intervals=l1[i]
            else: end_intervals=IntervalSet([l1[i]|l0[i]]) 
            new_intervals = []
            for interval in end_intervals:
                new_intervals.append(Interval(interval.start-vs.end*dl,interval.end-vs.start*dl))                            
            print('- l0', IntervalSet(new_intervals), dl)
            print(l0[i-1])   
            if i-1 in indices: l0[i-1]=IntervalSet([IntervalSet(new_intervals) & l0[i-1]])
            else: l0[i-1]=IntervalSet([IntervalSet(new_intervals) & l_old_start])
            print(l0[i-1])    

            if i in indices: end_intervals=l0[i]
            else: end_intervals=IntervalSet([l1[i]|l0[i]]) 
            new_intervals = []
            for interval in end_intervals:
                new_intervals.append(Interval(interval.start+vs.start*dl,interval.end+vs.end*dl))                         
            print('- l1', IntervalSet(new_intervals), dl)
            print(l1[i-1])   
            if i-1 in indices: l1[i-1]=IntervalSet([IntervalSet(new_intervals) & l1[i-1]])
            else: l1[i-1]=IntervalSet([IntervalSet(new_intervals) & l_old_start])
            print(l1[i-1])    

        


    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()



    def randFromIntervalSet(my_IntervalSet):
        chosen_interval = random.choice(list(my_IntervalSet))                   # я пока не прописала и не знаю по какому принципу выбирать, поэтому пусть будет рандом
        return random.randint(int(chosen_interval.start), int(chosen_interval.end))

    if (l1[0]|l0[0]) and (l1[-1]|l0[-1]):

        a = []  #массив, куда запишется то что нам надо для сценария из этой прелести, нумерация согласно dlit
        p = [randFromIntervalSet(start)]  #массив уже выбранных положений, нумерация согласно l

        for i in range(len(dlit)):
            dl=dlit[i]
            start_p = p[-1]

            
            if i+1 in indices:
                c = IntervalSet([l0[i+1]])
                d = IntervalSet([l1[i+1]])
            else:
                c = IntervalSet([l0[i+1]|l1[i+1]])
                d = c
            
            
            x = IntervalSet([c & IntervalSet([Interval(start_p-vs.end*dl,start_p-vs.start*dl)])])
            y = IntervalSet([d & IntervalSet([Interval(start_p+vs.start*dl,start_p+vs.end*dl)])])

            if i in indices: 
                if a[-1][0]: 
                    new_intervals = x
                else:
                    new_intervals = y

            else:
                
                if not i+1 in indices:
                    new_intervals = IntervalSet([IntervalSet([l1[i+1]|l0[i+1]]) & (Interval(start_p-vs.end*dl,start_p-vs.start*dl) | Interval(start_p+vs.start*dl,start_p+vs.end*dl))])
                else:
                    new_intervals = IntervalSet([x|y])
                

             
            p_predvarit = randFromIntervalSet(new_intervals)     # я пока не прописала и не знаю по какому принципу выбирать, поэтому пусть будет рандом

            v = round((p_predvarit-start_p)/dl)
            p.append(start_p+v*dl) 

            if not p[-1] in new_intervals:     # проверка на случай если при округлении скорости у нас точка вылезла за интервал. Мне было лень её прописывать нормально, так что придётся читать как есть
                v+=1
                pn=start_p+v*dl
                if not pn in new_intervals:
                    v-=2
                    pn=start_p+v*dl
                    if not pn in new_intervals:
                        v+=1
                        pn=p[-1]
                        print('Ой, а вот и то самое бутылоное горлышко, осторожно')
                p[-1]=pn


            a.append((int(v>0), dl, abs(v)))

            print(a[-1])    

def raspr_dyn_with_smych_to_good(dlit: list, indices, start: IntervalSet = IntervalSet([Interval(0,0)]), end: IntervalSet = IntervalSet([Interval(-1000,1000)]), were_can_be: IntervalSet = IntervalSet([Interval(0,100000)]), vs: Interval = Interval(48,133), good: IntervalSet = IntervalSet([Interval(0, 10000),Interval(80000, 900000)]), good_vs: IntervalSet = Interval(60, 100)) -> list: 

    # Здесь добавляется ещё одна характеристика, означающая предпочтительный интервал - по умолчанию (0,10 000) + (80 000, 90 000) - чтобы дотягивал до конца смычка если может
    # А также добавляется предпочтительный "хороший" интервал скоростей

    # индексы длительностей перед которыми нужна смена смычка
    if 0 in indices: indices.remove(0)

    #start = IntervalSet([Interval(0,0)])

    #end = IntervalSet([Interval(-1000,1000)])

    l1 = []     # дин. списки куда для каждого i записываются значения с которых нота может стартовать, i+1 - куда может прийти
    l0 = []                                         # start под 0 номером, end должен дать непустое пересечение с номером len(dlit)

    l1.append(start)                    # в l1 мы записываем те значения в которые пришли в + направлении
    l0.append(start)                    # в l0 - те в которые пришли в отрицательном направлении

    #were_can_be = IntervalSet([Interval(0,100000)])
    #vs = Interval(48,133)


    for i in range(len(dlit)):    #проход туда - понимаем прошли/не прошли, но не помним как. Помним зависимость только в одном направлении
        dl = dlit[i]                                   # т.е. для каждой точки здесь записываются те интервалы в коотрые мы можем прийти со старта
        
        if i in indices: start_intervals=l1[-1]          #сначала считаем для l0 - для них при необходимости смены смычка нам нужны предыдущие значения из l1
        else: start_intervals=IntervalSet([l1[-1]|l0[-1]]) 
        new_intervals = []
        for interval in start_intervals:
            new_intervals.append(Interval(interval.start-vs.end*dl,interval.end-vs.start*dl))
        print('-', IntervalSet(new_intervals), dl)
        l0.append(IntervalSet([IntervalSet(new_intervals) & were_can_be]))
        print(l0[-1])

        if i in indices: start_intervals=l0[-2]          #затем для l1 - здесь уже поменялся индекс у l0, т.к. мы в него кое-что добавили только что
        else: start_intervals=IntervalSet([l1[-1]|l0[-2]])
        new_intervals = []
        for interval in start_intervals:
            new_intervals.append(Interval(interval.start+vs.start*dl,interval.end+vs.end*dl))
        print('-', IntervalSet(new_intervals), dl)
        l1.append(IntervalSet([IntervalSet(new_intervals) & were_can_be]))
        print(l1[-1])


    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()

    l0_old = l0.copy()
    l1_old = l1.copy()

    if IntervalSet([(l1[-1]|l0[-1])]) & end:                            # а это проход обратно - и тут мы уже выбираем те точки, с которых можно дойти до конца - и сразу на каждом шагу выбираем из них только те, в которые можно дойти от начала (по уже существующим в списке интервалам)
        l1[-1] = IntervalSet( [l1[-1] & end])                    # таким образом у нас получается список, где мы в каждой точке есть положение, в которое гарантированно можно поставить смычок и начать играть в любую сторону - и всё будет хорошо
        l0[-1] = IntervalSet( [l0[-1] & end])                    # кстати теперь l1 у нас выполняет функцию того, откуда достоверно можно пойти в отрицательном направлении
        for i in range(len(l1)-1, 0, -1):                           # l0 - напротив функцию того, откуда можно пойти в положительном и достигнуть конца
            dl = dlit[i-1]
            print()
            print(i)
            l_old_start = IntervalSet([l0[i-1]|l1[i-1]])
            if i in indices: end_intervals=l1[i]
            else: end_intervals=IntervalSet([l1[i]|l0[i]]) 
            new_intervals = []
            new_good_V_intervals = []
            for interval in end_intervals:
                new_good_V_intervals.append(Interval(interval.start-good_vs.end*dl,interval.end-good_vs.start*dl))                            
                new_intervals.append(Interval(interval.start-vs.end*dl,interval.end-vs.start*dl))               
            print('- l0', IntervalSet(new_intervals), dl)
            print(l0[i-1])   
            if i-1 in indices: l0[i-1]=IntervalSet([IntervalSet(new_intervals) & l0[i-1]])
            else: l0[i-1]=IntervalSet([IntervalSet(new_intervals) & l_old_start])

            if i-1 in indices: new_good_V_intervals=IntervalSet([IntervalSet(new_good_V_intervals) & l0[i-1]])
            else: new_good_V_intervals=IntervalSet([IntervalSet(new_good_V_intervals) & l_old_start])
            if new_good_V_intervals: l0[i-1] = new_good_V_intervals
            
            if good & l0[i-1]: l0[i-1]=IntervalSet([good & l0[i-1]])
            print(l0[i-1])    

            if i in indices: end_intervals=l0[i]
            else: end_intervals=IntervalSet([l1[i]|l0[i]]) 
            new_intervals = []
            new_good_V_intervals = []
            for interval in end_intervals:
                new_good_V_intervals.append(Interval(interval.start+good_vs.start*dl,interval.end+good_vs.end*dl))
                new_intervals.append(Interval(interval.start+vs.start*dl,interval.end+vs.end*dl))                         
            print('- l1', IntervalSet(new_intervals), dl)
            print(l1[i-1])   
            
            if i-1 in indices: l1[i-1]=IntervalSet([IntervalSet(new_intervals) & l1[i-1]])
            else: l1[i-1]=IntervalSet([IntervalSet(new_intervals) & l_old_start])
            
            if i-1 in indices: new_good_V_intervals=IntervalSet([IntervalSet(new_good_V_intervals) & l1[i-1]])
            else: new_good_V_intervals=IntervalSet([IntervalSet(new_good_V_intervals) & l_old_start])
            if new_good_V_intervals: l1[i-1] = new_good_V_intervals

            if good & l1[i-1]: l1[i-1]=IntervalSet([good & l1[i-1]])      
            print(l1[i-1])    

        


    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()






    #if vis: plot_interval_sets(l0,l1)







    def randFromIntervalSet(my_IntervalSet):
        chosen_interval = random.choice(list(my_IntervalSet))                   # я пока не прописала и не знаю по какому принципу выбирать, поэтому пусть будет рандом
        return random.randint(int(chosen_interval.start), int(chosen_interval.end))
    


    try:
    

        if (l1[0]|l0[0]) and (l1[-1]|l0[-1]):

            a = []  #массив, куда запишется то что нам надо для сценария из этой прелести, нумерация согласно dlit
            p = [randFromIntervalSet(IntervalSet([l0[0]|l1[0]]))]  #массив уже выбранных положений, нумерация согласно l

            for i in range(len(dlit)):
                dl=dlit[i]
                start_p = p[-1]

                
                if i+1 in indices:
                    c = IntervalSet([l0[i+1]])
                    d = IntervalSet([l1[i+1]])
                else:
                    c = IntervalSet([l0[i+1]|l1[i+1]])
                    d = c
                
                
                #x = IntervalSet([c & IntervalSet([Interval(start_p-(vs.end+1)*dl,start_p-(vs.start-1)*dl)])])
                #y = IntervalSet([d & IntervalSet([Interval(start_p+(vs.start-1)*dl,start_p+(vs.end+1)*dl)])])

                x = IntervalSet([c & IntervalSet([Interval(start_p-(vs.end)*dl,start_p-(vs.start)*dl)])])
                y = IntervalSet([d & IntervalSet([Interval(start_p+(vs.start)*dl,start_p+(vs.end)*dl)])])

                if i in indices:
                    if a[-1][0]: 
                        new_intervals = x
                    else:
                        new_intervals = y
                else:
                    new_intervals = IntervalSet([x|y])
                    

                
                p_predvarit = randFromIntervalSet(new_intervals)     # я пока не прописала и не знаю по какому принципу выбирать, поэтому пусть будет рандом
                v = round((p_predvarit-start_p)/dl)

                if dl<300: 
                    ma = max(interval.end for interval in new_intervals)
                    mi = min(interval.start for interval in new_intervals)
                    v = max([round((p_predvarit-start_p)/dl) for v in [ma,mi]],key=abs)
                    
                                                    

                p.append(start_p+v*dl) 

                if not p[-1] in new_intervals:     # проверка на случай если при округлении скорости у нас точка вылезла за интервал. Мне было лень её прописывать нормально, так что придётся читать как есть
                    v+=1
                    pn=start_p+v*dl
                    if not pn in new_intervals:
                        v-=2
                        pn=start_p+v*dl
                        if not pn in new_intervals:
                            v+=1


                            pn=p_predvarit
                            print('Ой, а вот и то самое бутылоное горлышко, осторожно')
                    p[-1]=pn


                a.append((int(v>0), dl, abs(v)))

                print(a[-1]) 
 
            if vis: plot_interval_sets(l0,l1,p)
            return a  
        if vis: plot_interval_sets(l0,l1)
    except:
        if vis: plot_interval_sets(l0,l1,p)
        print(l1[63],l0[63])

if __name__=='__main__':
    dlit = [
        375, 375, 1125, 375, 375, 375, 1125, 375, 375, 375,
        1500, 750, 1666, 1500, 750, 1125, 375, 375, 375, 375,
        375, 750, 750, 1666, 375, 1666, 375, 1666, 375, 1666,
        375, 1666, 375, 1666, 375, 1666, 375, 1666, 375, 1125,
        375, 375, 375, 1125, 375, 375, 375, 1125, 375, 375,
        375, 1125, 375, 375, 375, 1125, 187, 187, 375, 375,
        1125, 375, 375, 375, 1125, 375, 375, 375, 1500, 750,
        1666, 1666, 375, 1125, 375, 375, 375, 375, 375, 750,
        750, 1666
    ]

    
    indices = [1, 3, 6, 10, 14, 15, 18, 19, 22, 23, 24, 25, 26, 27, 31, 32, 33, 37, 40, 44, 46, 54, 55, 57, 60, 64, 67, 68, 71, 72, 75, 76, 79]

    start = IntervalSet([Interval(0,0)])

    end = IntervalSet([Interval(-1000,1000)])


    were_can_be = IntervalSet([Interval(0,100000)])
    vs = Interval(48,133)

    raspr_dyn_with_smych_to_good(dlit[:10], indices)
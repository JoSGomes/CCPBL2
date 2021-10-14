def quickSort(dict):
   sort(dict,0,len(dict)-1)

def sort(dict,first,last):
   if first<last:

       split = getSplit(dict,first,last)

       sort(dict,first,split-1)
       sort(dict,split+1,last)
    

def getSplit(dict,first,last):
   pivot = dict[first]

   leftIndex = first+1
   rightIndex = last

   done = False
   while not done:
       while leftIndex <= rightIndex and dict[leftIndex]['sensor']['bloodOxygenation'] <= pivot['sensor']['bloodOxygenation']:
           leftIndex = leftIndex + 1

       while dict[rightIndex]['sensor']['bloodOxygenation'] >= pivot['sensor']['bloodOxygenation'] and rightIndex >= leftIndex:
           rightIndex = rightIndex -1

       if rightIndex < leftIndex:
           done = True
       else:
           temp = dict[leftIndex]
           dict[leftIndex] = dict[rightIndex]
           dict[rightIndex] = temp

   temp = dict[first]
   dict[first] = dict[rightIndex]
   dict[rightIndex] = temp


   return rightIndex
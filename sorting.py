def selection(a):
    for i in range(len(a)):
        le = i
        for k in range(i+1, len(a)):
            if a[k] < a[le]:
                le = k
                 
        swap(a, le, i)
         
def swap(c, x, y):
    temp = c[x]
    c[x] = c[y]
    c[y] = temp

my_list = [5.76,4.7,25.3,4.6,32.4,55.3,52.3,7.6,7.3,86.7,43.5]
selection(my_list)
print my_list

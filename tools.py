def progress(percent=0, width=30): #simple progress bar
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)

task = [i for i in range(1000)]
for i in range(len(task)):
	progress(int(i+1/n*100))
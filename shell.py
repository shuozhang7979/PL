import main

f = open('demo/test1.txt')
text = f.read()
res, error = main.run('f', text)
if error:
    print(error.as_string())
else:
    print(res)
